#!/usr/bin/env python3
"""
雅思口语自动化流程控制器
管理 Part 1 → Part 2 → Part 3 → 汇总 的完整流程
"""
import sys
import json
import os
import subprocess
from datetime import datetime

STATE_FILE = "/Users/curry/.openclaw/workspace/memory/ielts_session.json"
TRANSCRIPT_SCRIPT = "/Users/curry/.openclaw/skills/ielts-speaking/scripts/transcribe.py"

def load_state():
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def transcribe_audio(audio_path: str) -> tuple:
    """转写音频，返回 (transcript, duration_seconds)"""
    wav_path = f"/tmp/ielts_{os.getpid()}.wav"
    try:
        # 转换格式
        result = subprocess.run(
            ['python3', TRANSCRIPT_SCRIPT, audio_path, wav_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return "", 0.0
        
        with open(wav_path, 'r') as f:
            duration = float(f.read().strip())
        
        # 转写
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        import wave as wave_module
        
        with wave_module.open(wav_path, 'rb') as wf:
            data = wf.readframes(wf.getnframes())
            audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        
        processor = WhisperProcessor.from_pretrained('openai/whisper-base')
        model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-base')
        input_features = processor(audio, sampling_rate=16000, return_tensors='pt').input_features
        generated_ids = model.generate(input_features)
        transcript = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return transcript, duration
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

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
    """推进状态到下一题或下一Part"""
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
            # 进入 Part 2
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
            # 全部完成
            state['current_part'] = "DONE"
            return None, -1

    return None, -1

def init_session(test_info: dict):
    """初始化新的测试会话"""
    # 兼容 notion_search.py 的输出格式
    test_info = normalize_test_info(test_info)
    
    state = {
        "active": True,
        "test_number": test_info.get('test_number'),
        "test_info": test_info,
        "current_part": "Part 1",
        "current_q_index": 0,
        "part1": {"questions": test_info['Part 1'], "answers": []},
        "part2": {"topic": test_info.get('Part 2 题卡') or test_info.get('Part 2 topic', ''), "should_say": test_info.get('Part 2 should_say', []), "answer": ""},
        "part3": {"questions": test_info['Part 3'], "answers": []},
        "scores": {"part1": [], "part2": None, "part3": []},
        "analysis": {"part1": [], "part2": "", "part3": []},
        "started_at": datetime.now().isoformat()
    }
    save_state(state)
    return state


def normalize_test_info(info: dict) -> dict:
    """将 notion_search 输出标准化为内部格式"""
    # notion_search keys: test_number, title, topic_cn, Part 1, Part 2 topic, Part 2 should_say, Part 3, category, difficulty, page_id
    # 内部 keys: test_number, 题目, Part 1, Part 2 题卡, Part 2 should_say, Part 3, 类型, 难度
    result = dict(info)
    
    # 标题
    if '题目' not in result and 'title' in result:
        result['题目'] = result['title']
    
    # Part 2 题卡
    if 'Part 2 题卡' not in result and 'Part 2 topic' in result:
        result['Part 2 题卡'] = result['Part 2 topic']
    
    # 类型
    if '类型' not in result and 'category' in result:
        result['类型'] = result['category']
    
    # 难度
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
    part = state['current_part']
    q_idx = state['current_q_index']
    test_info = state['test_info']

    if part == "Part 1" and q_idx < len(test_info['Part 1']):
        return False
    if part == "Part 2" and not state['part2']['answer']:
        return False
    if part == "Part 3" and q_idx < len(test_info['Part 3']):
        # 已经回答完所有P3题？检查答案数量
        if len(state['part3']['answers']) >= len(test_info['Part 3']):
            return True  # 已完成
        return False
    if part == "DONE":
        return True
    return False

def generate_summary(state) -> str:
    """生成最终的汇总评分卡"""
    p1_scores = state['scores']['part1']
    p1_avg = sum(p1_scores) / len(p1_scores) if p1_scores else 0
    p2_band = state['scores']['part2'] or 0
    p3_scores = state['scores']['part3']
    p3_avg = sum(p3_scores) / len(p3_scores) if p3_scores else 0
    
    # 综合Band: Part1单独 + (Part2×40% + Part3×60%)加权
    # Part2+3合成 = Part2×0.4 + Part3×0.6
    # Overall = Part1×30% + Part2_3×70%
    p2_3_combined = p2_band * 0.4 + p3_avg * 0.6
    overall = p1_avg * 0.3 + p2_3_combined * 0.7
    
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
    """生成写入Notion的内容 - 升级版详细格式"""
    p1_scores = state['scores']['part1']
    p1_avg = sum(p1_scores) / len(p1_scores) if p1_scores else 0
    p2_band = state['scores']['part2'] or 0
    p3_scores = state['scores']['part3']
    p3_avg = sum(p3_scores) / len(p3_scores) if p3_scores else 0
    p2_3_combined = p2_band * 0.4 + p3_avg * 0.6
    overall = p1_avg * 0.3 + p2_3_combined * 0.7

    # 构建 Part 1 详细分析
    part1_detailed = []
    for ans in state['part1']['answers']:
        ana = ans.get('analysis', {})
        # 解析analysis字符串为结构化数据
        if isinstance(ana, str):
            ana = parse_analysis_string(ana)
        part1_detailed.append({
            "question": ans['question'],
            "transcript": ans['transcript'],
            "band": ans['band'],
            "analysis": ana
        })

    # Part 2 详细分析
    part2_ana = state['analysis'].get('part2', {})
    if isinstance(part2_ana, str):
        part2_ana = parse_analysis_string(part2_ana)

    # 构建 Part 3 详细分析
    part3_detailed = []
    for ans in state['part3']['answers']:
        ana = ans.get('analysis', {})
        if isinstance(ana, str):
            ana = parse_analysis_string(ana)
        part3_detailed.append({
            "question": ans['question'],
            "transcript": ans['transcript'],
            "band": ans['band'],
            "analysis": ana
        })

    # 生成总结
    all_bands = p1_scores + [p2_band] + p3_scores
    summary = generate_summary_text(state, p1_avg, p2_band, p3_avg)

    return {
        "student_nickname": "Caleb Chen",
        "topic_category": state['test_info'].get('类型', ''),
        "topic_short_id": f"Test {state['test_info'].get('test_number', ''):02d}",
        "topic_en": state['test_info'].get('Part 2 题卡', ''),
        "test_num": state['test_info'].get('test_number', 0),
        "overall_band": round(overall, 1),
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
            "part3": part3_detailed,
            "summary": summary
        }
    }


def parse_analysis_string(ana_str: str) -> dict:
    """解析 analysis 字符串为结构化字典"""
    if isinstance(ana_str, dict):
        return ana_str
    # 尝试从字符串中提取各项
    result = {
        "grammar": "",
        "vocabulary": "",
        "logic": "",
        "ideas": "",
        "basic_fix": "",
        "满分升级": "",
        "考官点拨": ""
    }
    if not ana_str:
        return result
    # 简单解析：如果有band信息
    if 'band' in ana_str.lower():
        import re
        m = re.search(r'"band":\s*([\d.]+)', ana_str)
        if m:
            result["band"] = float(m.group(1))
    return result


def generate_summary_text(state, p1_avg, p2_band, p3_avg) -> dict:
    """生成综合表现总结"""
    # 分析各部分表现
    p1_scores = state['scores']['part1']
    p3_scores = state['scores']['part3']

    # 找出最高和最低
    all_scores = p1_scores + [p2_band] + p3_scores
    if all_scores:
        max_score = max(all_scores)
        min_score = min(all_scores)
    else:
        max_score = min_score = 0

    # 优势分析（得分较高的部分）
    advantages = []
    if p1_avg >= 5.5:
        advantages.append("Part 1 表达流畅，能就日常话题进行持续性讨论")
    if p2_band >= 5.5:
        advantages.append("Part 2 陈述结构完整，能覆盖所有要点")
    if p3_avg >= 5.5:
        advantages.append("Part 3 展现一定批判性思维，能就抽象话题展开讨论")
    if not advantages:
        advantages.append("整体表达意愿积极，敢于用英语交流")

    # 致命失分点
    weaknesses = []
    if p1_avg < 5.0:
        weaknesses.append("Part 1 语法错误较多，时态和单复数问题明显")
    if p2_band < 5.0:
        weaknesses.append("Part 2 逻辑连贯性不足，观点展开不够充分")
    if p3_avg < 5.0:
        weaknesses.append("Part 3 思路较浅，缺乏深度分析和举例论证")
    # 检查词汇问题
    for ans in state['part1']['answers']:
        ana = ans.get('analysis', {})
        if isinstance(ana, dict) and 'vocabulary' in ana:
            if '中式' in ana.get('vocabulary', '') or '简单' in ana.get('vocabulary', ''):
                weaknesses.append("词汇地道性不足，中式英语表达较多")
                break
    if not weaknesses:
        weaknesses.append("整体语法稳定性有待加强，部分句子出现混乱")

    # Action Plan
    actions = [
        "每日朗读剑桥雅思口语满分答案30分钟，重点模仿发音和语调",
        "系统复习时态用法：过去时、现在完成时、过去完成时",
        "积累各话题高分手势词汇替换（如 important → crucial, significant）",
        "练习使用连接词（however, moreover, consequently）提升逻辑连贯性"
    ]

    return {
        "优势": "；".join(advantages),
        "致命失分点": "；".join(weaknesses[:3]),
        "action_plan": "；".join(actions)
    }

# 命令行接口
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "init":
        # python3 ielts_flow.py init '<json_test_info>'
        test_info = json.loads(sys.argv[2])
        state = init_session(test_info)
        q_text, _ = get_next_question(state)
        print(q_text)
    
    elif cmd == "status":
        state = load_state()
        print(json.dumps(state, ensure_ascii=False, indent=2))
    
    elif cmd == "next":
        state = load_state()
        part_text, q_idx = advance_state(state)
        save_state(state)
        if part_text:
            print(part_text)
        else:
            print("DONE")
    
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
            content = generate_notion_content(state)
            # 写入临时文件，不在群里显示JSON
            notion_file = '/tmp/ielts_notion_pending.json'
            with open(notion_file, 'w') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f'Notion内容已生成，共 {len(content.get("evaluation", {}).get("part1", []))} 道Part1题，{len(content.get("evaluation", {}).get("part3", []))} 道Part3题')

    elif cmd == "notion_push":
        # python3 ielts_flow.py notion_push
        # 生成notion内容并直接写入Notion作业反馈库
        state = load_state()
        if not state.get('active') and not state.get('current_part') == 'DONE':
            print('ERROR: No completed session to push')
            sys.exit(1)

        content = generate_notion_content(state)

        # 调用notion_append_homework.py写入
        import subprocess
        proc = subprocess.Popen(
            ['python3', '/Users/curry/.openclaw/skills/ielts-speaking/scripts/notion_append_homework.py'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(json.dumps(content, ensure_ascii=False).encode(), timeout=30)
        result = type('Result', (), {'returncode': proc.returncode, 'stdout': stdout, 'stderr': stderr})()
        if result.returncode == 0:
            try:
                resp = json.loads(result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout)
                if resp.get('ok'):
                    print(f'✅ Notion写入成功！page_id: {resp.get("page_id", "")}')
                else:
                    print(f'❌ Notion写入失败: {resp}')
            except:
                print(f'❌ Notion写入失败: {result.stdout}')
        else:
            print(f'❌ Notion写入失败: {result.stderr[:500]}')
    
    elif cmd == "process":
        # python3 ielts_flow.py process <audio_path> <transcript> <duration> <analysis_json> <band>
        audio_path = sys.argv[2]
        transcript = sys.argv[3]
        duration = float(sys.argv[4])
        analysis = json.loads(sys.argv[5])
        band = float(sys.argv[6])

        state = load_state()
        if not state.get('active'):
            print('ERROR: No active session. Send /题目 Test XX to start.')
            sys.exit(1)

        state = process_answer(state, transcript, duration, analysis, band)

        # 检查是否完成
        if is_complete(state):
            state['current_part'] = "DONE"
            save_state(state)
            print("COMPLETE")
        else:
            part_text, q_idx = advance_state(state)
            save_state(state)
            print(part_text or "DONE")
    
    elif cmd == "reset":
        state = {"active": False, "test_number": None, "test_info": None,
                 "current_part": None, "current_q_index": 0,
                 "part1": {"questions": [], "answers": []},
                 "part2": {"topic": "", "should_say": [], "answer": ""},
                 "part3": {"questions": [], "answers": []},
                 "scores": {"part1": [], "part2": None, "part3": []},
                 "analysis": {"part1": [], "part2": "", "part3": []}}
        save_state(state)
        print("Reset complete")

    elif cmd == "analyze":
        # python3 ielts_flow.py analyze '<transcript>'
        transcript = sys.argv[2] if len(sys.argv) > 2 else ''
        if not transcript:
            print(json.dumps({"error": "No transcript provided"}))
        else:
            import subprocess
            result = subprocess.run(
                ['python3', '/Users/curry/.openclaw/skills/ielts-speaking/scripts/analyze_transcript.py', transcript],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                try:
                    analysis = json.loads(result.stdout)
                    print(json.dumps(analysis, ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    print(json.dumps({"error": "Failed to parse analysis result"}))
            else:
                print(json.dumps({"error": result.stderr}))

    elif cmd == "process_auto":
        # python3 ielts_flow.py process_auto <audio_path>
        # 自动转写 + 分析 + 处理答案
        audio_path = sys.argv[2] if len(sys.argv) > 2 else ''
        if not audio_path:
            print('ERROR: No audio file provided')
            sys.exit(1)

        state = load_state()
        if not state.get('active'):
            print('ERROR: No active session. Send /题目 Test XX to start.')
            sys.exit(1)

        # Step 1: 转写
        import subprocess
        wav_result = subprocess.run(
            ['python3', '/Users/curry/.openclaw/skills/ielts-speaking/scripts/transcribe.py', audio_path, '/tmp/auto_transcribe.wav'],
            capture_output=True, text=True, timeout=30
        )
        if wav_result.returncode != 0:
            print('ERROR: Audio conversion failed')
            sys.exit(1)

        # 读取时长
        try:
            with open('/tmp/auto_transcribe.wav', 'r') as f:
                duration = float(f.read().strip())
        except:
            duration = 0.0

        # Step 2: Whisper转写
        import numpy as np, wave as wave_module
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        with wave_module.open('/tmp/auto_transcribe.wav', 'rb') as wf:
            audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        processor = WhisperProcessor.from_pretrained('openai/whisper-base')
        model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-base')
        input_features = processor(audio, sampling_rate=16000, return_tensors='pt').input_features
        generated_ids = model.generate(input_features)
        transcript = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Step 3: AI分析（静默，不输出到群）
        analysis_result = subprocess.run(
            ['python3', '/Users/curry/.openclaw/skills/ielts-speaking/scripts/analyze_transcript.py', transcript],
            capture_output=True, text=True, timeout=30
        )
        if analysis_result.returncode != 0:
            sys.exit(1)

        try:
            analysis_data = json.loads(analysis_result.stdout)
        except:
            sys.exit(1)

        band = analysis_data.get('band', 5.5)

        # Step 4: 处理答案
        state = process_answer(state, transcript, duration, analysis_data, band)

        # 检查是否完成
        if is_complete(state):
            state['current_part'] = "DONE"
            save_state(state)
            print("COMPLETE")

            # 自动写入Notion（静默模式，不被 Whisper warnings 干扰）
            import subprocess
            content = generate_notion_content(state)
            notion_proc = subprocess.Popen(
                ['python3', '/Users/curry/.openclaw/skills/ielts-speaking/scripts/notion_append_homework.py'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            stdout, _ = notion_proc.communicate(json.dumps(content, ensure_ascii=False).encode(), timeout=30)
            try:
                resp = json.loads(stdout.decode() if isinstance(stdout, bytes) else stdout)
                if resp.get('ok'):
                    print(f'\n✅ Notion已自动写入: {resp.get("page_id", "")}')
                else:
                    print(f'\n❌ Notion写入失败，请手动运行 /notion_push')
            except:
                print(f'\n❌ Notion写入失败，请手动运行 /notion_push')
        else:
            part_text, q_idx = advance_state(state)
            save_state(state)
            print(part_text or "DONE")
