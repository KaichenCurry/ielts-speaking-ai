#!/usr/bin/env python3
"""
ielts_flow.py - 雅思口语 AI 助教系统 - 主流程控制器

管理 Part 1 → Part 2 → Part 3 → 汇总 的完整流程

使用方法：
    python3 ielts_flow.py init '<test_info_json>'
    python3 ielts_flow.py process <audio_path>
    python3 ielts_flow.py summary
    python3 ielts_flow.py status

环境变量（必需）：
    TELEGRAM_BOT_TOKEN
    MINIMAX_API_KEY
    NOTION_TOKEN

相对路径说明：
    状态文件：./memory/ielts_session.json
    脚本目录：./scripts/（与本文件同目录）
"""

import sys
import json
import os
import subprocess
from datetime import datetime

# ==========================================
# 路径配置（使用相对路径，支持项目目录任意位置）
# ==========================================

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 状态文件路径（./memory/ielts_session.json）
STATE_FILE = os.path.join(PROJECT_ROOT, "memory", "ielts_session.json")

# 确保 memory 目录存在
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

# 依赖脚本路径
TRANSCRIBE_SCRIPT = os.path.join(SCRIPT_DIR, "transcribe.py")
ANALYZE_SCRIPT = os.path.join(SCRIPT_DIR, "analyze_transcript.py")
NOTION_HOMEWORK_SCRIPT = os.path.join(SCRIPT_DIR, "notion_append_homework.py")

# ==========================================
# Band Score 计算公式（统一，所有文件共用此逻辑）
# ==========================================
# 
# 综合 Band = Part1×30% + (Part2×40% + Part3×60%)×70%
#
# 公式说明：
#   Part2_3 合成 = Part2×0.4 + Part3×0.6
#   Overall = Part1×0.3 + Part2_3×0.7
#
# 示例：
#   Part1 均分 = 6.0
#   Part2 得分 = 6.5
#   Part3 均分 = 6.0
#   
#   Part2_3 合成 = 6.5×0.4 + 6.0×0.6 = 2.6 + 3.6 = 6.2
#   Overall = 6.0×0.3 + 6.2×0.7 = 1.8 + 4.34 = 6.14 ≈ 6.0

def calculate_band(p1_avg: float, p2_score: float, p3_avg: float) -> float:
    """
    计算综合 Band Score
    
    Args:
        p1_avg: Part 1 平均分
        p2_score: Part 2 得分
        p3_avg: Part 3 平均分
    
    Returns:
        float: 综合 Band Score（保留 1 位小数）
    """
    p2_3_combined = p2_score * 0.4 + p3_avg * 0.6
    overall = p1_avg * 0.3 + p2_3_combined * 0.7
    return round(overall, 1)

# ==========================================
# 状态管理
# ==========================================

def load_state():
    """加载状态文件"""
    if not os.path.exists(STATE_FILE):
        return {"active": False}
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    """保存状态文件"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ==========================================
# 音频处理
# ==========================================

def convert_audio_to_wav(audio_path: str) -> tuple:
    """
    将音频转换为 WAV 格式
    
    Returns:
        tuple: (wav_path, duration_seconds)
    """
    wav_path = f"/tmp/ielts_{os.getpid()}.wav"
    try:
        result = subprocess.run(
            ['python3', TRANSCRIBE_SCRIPT, audio_path, wav_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return "", 0.0
        
        with open(wav_path, 'r') as f:
            duration = float(f.read().strip())
        
        return wav_path, duration
    except Exception:
        return "", 0.0

def transcribe_with_whisper(wav_path: str) -> str:
    """
    使用 Whisper 模型转写音频
    
    依赖：transformers, torch, numpy
    
    Returns:
        str: 转写文本
    """
    try:
        import numpy as np
        import wave as wave_module
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        
        with wave_module.open(wav_path, 'rb') as wf:
            data = wf.readframes(wf.getnframes())
            audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        
        processor = WhisperProcessor.from_pretrained('openai/whisper-base')
        model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-base')
        input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features
        generated_ids = model.generate(input_features)
        transcript = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return transcript
    except ImportError as e:
        print(f"警告：Whisper 模型未安装，使用备用转写: {e}", file=sys.stderr)
        return ""

# ==========================================
# AI 评分（调用 MiniMax）
# ==========================================

def analyze_with_minimax(transcript: str, topic: str = "") -> dict:
    """
    使用 MiniMax 大语言模型进行评分
    
    依赖：MINIMAX_API_KEY 环境变量
    
    Args:
        transcript: 学生答题转写文本
        topic: 话题关键词（用于 RAG 增强）
    
    Returns:
        dict: {"analysis": str, "band": float}
    """
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key or api_key == "YOUR_MINIMAX_API_KEY":
        # 备用：使用本地分析
        return analyze_locally(transcript)
    
    # RAG 增强上下文
    rag_context = ""
    if topic:
        try:
            rag_result = subprocess.run(
                ['python3', os.path.join(SCRIPT_DIR, "rag_retrieve.py"), topic],
                capture_output=True, text=True, timeout=10
            )
            if rag_result.returncode == 0:
                rag_context = rag_result.stdout
        except Exception:
            pass
    
    # 调用 MiniMax API
    try:
        import urllib.request
        import urllib.parse
        
        payload = {
            "model": "MiniMax-Abab6.5s",
            "messages": [
                {
                    "role": "system",
                    "content": f"""你是一个雅思口语评分助手。请根据以下评分标准对学生的口语回答进行评分：

评分维度（每句话都要分析）：
- 语法：主谓一致、从句使用、介词搭配
- 词汇：Chinglish、高分替换、地道表达
- 时态：过去时、现在时、完成时
- 逻辑：因果关系、转折、层次感
- 思路：举例具体性、论证深度

Band Score 参考：
- 9分：接近母语者水平
- 7-8分：表达流畅，偶有错误
- 5-6分：能表达意思，但有明显错误
- 4分以下：表达困难，错误严重影响理解

历史类似话题参考：
{rag_context if rag_context else '无'}

请输出：
1. 逐句分析（每句话的5维度评价）
2. 综合 Band Score（0.5分为单位）
3. 主要问题总结"""
                },
                {
                    "role": "user",
                    "content": f"学生回答：\n{transcript}"
                }
            ]
        }
        
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            "https://api.minimax.chat/v1/text/chatcompletion_pro",
            data=data,
            method="POST"
        )
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.load(resp)
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 尝试从内容中提取 Band Score
            import re
            band_match = re.search(r'(\d+\.?\d?)\s*(分|score|band)', content)
            band = float(band_match.group(1)) if band_match else 6.0
            
            return {"analysis": content, "band": band}
    
    except Exception as e:
        print(f"MiniMax API 调用失败，使用本地分析: {e}", file=sys.stderr)
        return analyze_locally(transcript)

def analyze_locally(transcript: str) -> dict:
    """
    本地备用分析（当 MiniMax API 不可用时）
    
    调用 analyze_transcript.py 进行评分
    """
    try:
        result = subprocess.run(
            ['python3', ANALYZE_SCRIPT, transcript],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {"analysis": json.dumps(data, ensure_ascii=False), "band": data.get("band", 6.0)}
    except Exception:
        pass
    
    return {"analysis": "分析不可用", "band": 6.0}

# ==========================================
# 流程控制
# ==========================================

def get_next_question(state):
    """根据当前状态返回下一道题"""
    part = state['current_part']
    q_idx = state['current_q_index']
    
    if part == "Part 1":
        qs = state['test_info']['Part 1']
        if q_idx < len(qs):
            return f"Q{q_idx+1}: {qs[q_idx]}", q_idx + 1
    elif part == "Part 2":
        return "Part 2", -1
    elif part == "Part 3":
        qs = state['test_info']['Part 3']
        if q_idx < len(qs):
            return f"Q{q_idx+1}: {qs[q_idx]}", q_idx + 1
    return None, -1

def advance_state(state, part_override=None):
    """推进状态到下一题或下一 Part"""
    part = part_override or state['current_part']
    q_idx = state['current_q_index']
    test_info = state['test_info']
    
    if part == "Part 1":
        next_q_idx = q_idx + 1
        if next_q_idx < len(test_info['Part 1']):
            state['current_part'] = "Part 1"
            state['current_q_index'] = next_q_idx
            return f"Part 1 - 第{next_q_idx+1}题（共{len(test_info['Part 1'])}题）", next_q_idx
        else:
            state['current_part'] = "Part 2"
            state['current_q_index'] = 0
            return "Part 2", -1

    elif part == "Part 2":
        state['current_part'] = "Part 3"
        state['current_q_index'] = 0
        return f"Part 3 - 第1题（共{len(test_info['Part 3'])}题）", 0

    elif part == "Part 3":
        next_q_idx = q_idx + 1
        if next_q_idx < len(test_info['Part 3']):
            state['current_part'] = "Part 3"
            state['current_q_index'] = next_q_idx
            return f"Part 3 - 第{next_q_idx+1}题（共{len(test_info['Part 3'])}题）", next_q_idx
        else:
            state['current_part'] = "DONE"
            return None, -1

    return None, -1

# ==========================================
# 会话管理
# ==========================================

def init_session(test_info: dict):
    """初始化新的测试会话"""
    test_info = normalize_test_info(test_info)
    
    state = {
        "active": True,
        "test_number": test_info.get('test_number'),
        "test_info": test_info,
        "current_part": "Part 1",
        "current_q_index": 0,
        "part1": {"questions": test_info['Part 1'], "answers": []},
        "part2": {
            "topic": test_info.get('Part 2 题卡') or test_info.get('Part 2 topic', ''),
            "should_say": test_info.get('Part 2 should_say', []),
            "answer": ""
        },
        "part3": {"questions": test_info['Part 3'], "answers": []},
        "scores": {"part1": [], "part2": None, "part3": []},
        "analysis": {"part1": [], "part2": "", "part3": []},
        "started_at": datetime.now().isoformat()
    }
    save_state(state)
    return state

def normalize_test_info(info: dict) -> dict:
    """将 notion_search 输出标准化为内部格式"""
    result = dict(info)
    
    if '题目' not in result and 'title' in result:
        result['题目'] = result['title']
    if 'Part 2 题卡' not in result and 'Part 2 topic' in result:
        result['Part 2 题卡'] = result['Part 2 topic']
    if '类型' not in result and 'category' in result:
        result['类型'] = result['category']
    if '难度' not in result and 'difficulty' in result:
        result['难度'] = result['difficulty']
    
    return result

def process_answer(state, transcript: str, duration: float, analysis: dict, band: float):
    """处理学生答案，存储结果"""
    part = state['current_part']
    q_idx = state['current_q_index']
    
    if part == "Part 1":
        state['part1']['answers'].append({
            "question": state['part1']['questions'][q_idx],
            "transcript": transcript,
            "duration_s": duration,
            "analysis": analysis,
            "band": band
        })
        state['scores']['part1'].append(band)
        state['analysis']['part1'].append(analysis)
    elif part == "Part 2":
        state['part2']['answer'] = transcript
        state['scores']['part2'] = band
        state['analysis']['part2'] = analysis
    elif part == "Part 3":
        state['part3']['answers'].append({
            "question": state['part3']['questions'][q_idx],
            "transcript": transcript,
            "duration_s": duration,
            "analysis": analysis,
            "band": band
        })
        state['scores']['part3'].append(band)
        state['analysis']['part3'].append(analysis)
    
    save_state(state)
    return state

def is_complete(state):
    """检查会话是否完成"""
    part = state['current_part']
    q_idx = state['current_q_index']
    test_info = state['test_info']

    if part == "Part 1" and q_idx < len(test_info['Part 1']):
        return False
    if part == "Part 2" and not state['part2']['answer']:
        return False
    if part == "Part 3" and q_idx < len(test_info['Part 3']):
        if len(state['part3']['answers']) >= len(test_info['Part 3']):
            return True
        return False
    if part == "DONE":
        return True
    return False

# ==========================================
# 结果生成
# ==========================================

def generate_summary(state) -> str:
    """生成最终的汇总评分卡"""
    p1_scores = state['scores']['part1']
    p1_avg = sum(p1_scores) / len(p1_scores) if p1_scores else 0
    p2_band = state['scores']['part2'] or 0
    p3_scores = state['scores']['part3']
    p3_avg = sum(p3_scores) / len(p3_scores) if p3_scores else 0
    
    # 使用统一的 Band 计算公式
    overall = calculate_band(p1_avg, p2_band, p3_avg)
    
    lines = []
    lines.append("=" * 50)
    lines.append("📊 IELTS 口语评分汇总")
    lines.append("=" * 50)
    lines.append(f"题目：{state['test_info']['题目']}")
    lines.append("")
    lines.append(f"🎤 Part 1 均分：{p1_avg:.1f} / 9.0")
    lines.append(f"📝 Part 2 得分：{p2_band:.1f} / 9.0")
    lines.append(f"🔍 Part 3 均分：{p3_avg:.1f} / 9.0")
    lines.append("")
    lines.append(f"🏆 综合 Band Score：{overall:.1f} / 9.0")
    lines.append("=" * 50)
    
    return "\n".join(lines)

def generate_notion_content(state) -> dict:
    """生成写入 Notion 的内容"""
    p1_scores = state['scores']['part1']
    p1_avg = sum(p1_scores) / len(p1_scores) if p1_scores else 0
    p2_band = state['scores']['part2'] or 0
    p3_scores = state['scores']['part3']
    p3_avg = sum(p3_scores) / len(p3_scores) if p3_scores else 0
    
    # 使用统一的 Band 计算公式
    overall = calculate_band(p1_avg, p2_band, p3_avg)
    
    # 构建各部分详细分析
    part1_detailed = []
    for ans in state['part1']['answers']:
        ana = ans.get('analysis', {})
        if isinstance(ana, dict):
            part1_detailed.append({
                "question": ans['question'],
                "transcript": ans['transcript'],
                "band": ans['band'],
                "analysis": ana
            })

    part2_ana = state['analysis'].get('part2', {})
    if isinstance(part2_ana, str):
        part2_ana = parse_analysis_string(part2_ana)

    part3_detailed = []
    for ans in state['part3']['answers']:
        ana = ans.get('analysis', {})
        if isinstance(ana, dict):
            part3_detailed.append({
                "question": ans['question'],
                "transcript": ans['transcript'],
                "band": ans['band'],
                "analysis": ana
            })

    return {
        "student_nickname": "学生",
        "topic_category": state['test_info'].get('类型', ''),
        "topic_short_id": f"Test {state['test_info'].get('test_number', ''):02d}",
        "topic_en": state['test_info'].get('Part 2 题卡', ''),
        "test_num": state['test_info'].get('test_number', 0),
        "overall_band": overall,
        "scores": {
            "part1_avg": round(p1_avg, 1),
            "part2": round(p2_band, 1),
            "part3_avg": round(p3_avg, 1)
        },
        "evaluation": {
            "part1": part1_detailed,
            "part2": {
                "transcript": state['part2']['answer'],
                "band": p2_band,
                "analysis": part2_ana
            },
            "part3": part3_detailed
        }
    }

def parse_analysis_string(ana_str: str) -> dict:
    """解析 analysis 字符串为结构化字典"""
    if isinstance(ana_str, dict):
        return ana_str
    result = {
        "grammar": "", "vocabulary": "", "logic": "",
        "ideas": "", "basic_fix": "", "满分升级": "", "考官点拨": ""
    }
    if not ana_str:
        return result
    import re
    m = re.search(r'"band":\s*([\d.]+)', ana_str)
    if m:
        result["band"] = float(m.group(1))
    return result

def write_to_notion(state):
    """写入 Notion 作业反馈库"""
    content = generate_notion_content(state)
    
    if os.path.exists(NOTION_HOMEWORK_SCRIPT):
        try:
            proc = subprocess.Popen(
                ['python3', NOTION_HOMEWORK_SCRIPT],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate(
                json.dumps(content, ensure_ascii=False).encode(),
                timeout=30
            )
            if proc.returncode == 0:
                try:
                    resp = json.loads(stdout.decode() if isinstance(stdout, bytes) else stdout)
                    if resp.get('ok'):
                        return f"✅ Notion写入成功！page_id: {resp.get('page_id', '')}"
                except:
                    pass
        except Exception as e:
            return f"❌ Notion写入失败: {e}"
    
    return "⚠️ Notion写入脚本不存在，请检查部署"

# ==========================================
# 命令行接口
# ==========================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 ielts_flow.py <command> [args]")
        print("命令:")
        print("  init '<json>'     - 初始化会话")
        print("  process <audio>  - 处理音频（自动转写+评分）")
        print("  summary          - 显示评分汇总")
        print("  status           - 显示当前状态")
        print("  notion           - 写入Notion")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "init":
        test_info = json.loads(sys.argv[2])
        state = init_session(test_info)
        q_text, _ = get_next_question(state)
        print(q_text)
    
    elif cmd == "status":
        state = load_state()
        print(json.dumps(state, ensure_ascii=False, indent=2))
    
    elif cmd == "summary":
        state = load_state()
        if not state.get('active'):
            print('No active session')
        else:
            print(generate_summary(state))
    
    elif cmd == "notion":
        state = load_state()
        if not state.get('active'):
            print(json.dumps({'error': 'No active session'}))
        else:
            print(write_to_notion(state))
    
    elif cmd == "process":
        # python3 ielts_flow.py process <audio_path>
        audio_path = sys.argv[2] if len(sys.argv) > 2 else ''
        if not audio_path:
            print('ERROR: No audio file provided')
            sys.exit(1)

        state = load_state()
        if not state.get('active'):
            print('ERROR: No active session. Run "init" first.')
            sys.exit(1)

        # Step 1: 转换音频
        wav_path, duration = convert_audio_to_wav(audio_path)
        if not wav_path:
            print('ERROR: Audio conversion failed')
            sys.exit(1)

        # Step 2: Whisper 转写
        transcript = transcribe_with_whisper(wav_path)
        
        # Step 3: AI 评分（MiniMax 或本地备用）
        topic = state['test_info'].get('Part 2 题卡', '')
        result = analyze_with_minimax(transcript, topic)
        analysis = result["analysis"]
        band = result["band"]

        # Step 4: 处理答案
        state = process_answer(state, transcript, duration, analysis, band)

        # 清理临时文件
        if os.path.exists(wav_path):
            os.remove(wav_path)

        # 检查是否完成
        if is_complete(state):
            state['current_part'] = "DONE"
            save_state(state)
            print("COMPLETE")
            print(write_to_notion(state))
        else:
            part_text, q_idx = advance_state(state)
            save_state(state)
            print(part_text or "DONE")
    
    elif cmd == "reset":
        state = {
            "active": False, "test_number": None, "test_info": None,
            "current_part": None, "current_q_index": 0,
            "part1": {"questions": [], "answers": []},
            "part2": {"topic": "", "should_say": [], "answer": ""},
            "part3": {"questions": [], "answers": []},
            "scores": {"part1": [], "part2": None, "part3": []},
            "analysis": {"part1": [], "part2": "", "part3": []}
        }
        save_state(state)
        print("Reset complete")
