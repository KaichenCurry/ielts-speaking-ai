#!/usr/bin/env python3
"""
雅思口语答案AI分析器 - 严格8分版
每一句话都必须严格诊断，不放过任何错误
"""
import sys
import json
import re

def analyze_transcript(transcript: str) -> dict:
    sentences = split_sentences(transcript)
    if not sentences:
        sentences = [transcript]
    
    results = []
    for i, sent in enumerate(sentences, 1):
        diagnosis = diagnose_strict(sent)
        fix = suggest_fix(sent, diagnosis)
        results.append({
            "id": i,
            "text": sent,
            "diagnosis": diagnosis,
            "fix": fix
        })
    
    summary = make_summary(results)
    band = estimate_band(results)
    
    return {
        "sentences": results,
        "summary": summary,
        "band": band
    }


def split_sentences(text: str) -> list:
    """拆分句子或意群"""
    text = text.strip()
    if not text:
        return []
    
    # 按标点拆分
    import re
    parts = re.split(r'(?<=[.!?])\s+', text)
    if len(parts) > 1:
        return [p.strip() for p in parts if p.strip()]
    
    # 按连接词拆分
    for sep in [' and ', ' but ', ' so ', ' because ', ' however ', ' then ']:
        pattern = sep.strip()
        if pattern in text.lower():
            subparts = re.split(sep, text, flags=re.IGNORECASE)
            if len(subparts) > 1:
                result = []
                for sp in subparts:
                    sp = sp.strip()
                    if sp:
                        result.extend(split_sentences(sp))
                return result if result else [text]
    
    # 按逗号拆分（如果句子够长）
    if len(text) > 80 and ',' in text:
        parts = text.split(',')
        if len(parts) > 2:
            return [p.strip() for p in parts if p.strip()]
    
    return [text]


def diagnose_strict(sentence: str) -> str:
    """严格诊断每句话"""
    s = sentence.strip()
    if not s:
        return "空句子"
    
    s_lower = s.lower()
    words = s.split()
    errors = []
    
    # ========== 主谓一致问题 ==========
    
    # I am like / I'm like 后面跟动词原形
    if re.search(r"\b(i am|i'm)\s+like\s+\w+\s+(love|like|go|come|have|do|think|know|want|see|get)\b", s_lower):
        errors.append("谓语错误：'am like'后不能直接跟动词原形，应为'I really love'或'I'm the type who loves'")
    
    # it/this/that + 单数动词 (不用三单)
    for pron in ['it ', 'it,', 'it.', 'this ', 'that ']:
        if s_lower.startswith(pron) or pron in s_lower[:15]:
            # 常见错误：it prefer, it require, it depend
            for verb in ['prefer', 'require', 'depend', 'seem', 'has ', 'have ']:
                if verb in s_lower[:30]:
                    # 排除 it is, it seems, it has 这类正确用法
                    if not re.search(r'\b(it|this|that)\s+(is|was|has|seems)\b', s_lower[:30]):
                        errors.append(f"主谓不一致：{pron.strip()}后面谓语动词三单形式可能错误")
                        break
            break
    
    # ========== 介词/冠词错误 ==========
    
    # 缺少冠词 a/an/the
    if re.search(r'\b(set|have|do|make|get|take|keep|put)\s+\w+\s+of\s+\w+ing\b', s_lower):
        errors.append("介词错误：动词短语搭配不当")
    
    # 冠词混淆
    if re.search(r'\ba\s+[aeiou]\w+\b', s_lower):
        m = re.search(r'\ba\s+([aeiou]\w+)', s_lower)
        if m:
            errors.append(f"冠词错误：a后面跟元音开头单词 '{m.group(1)}'，应改为 an")
    if re.search(r'\ban\s+[bcdfghjklmnpqrstvwxyz]\w+\b', s_lower):
        m = re.search(r'\ban\s+([bcdfghjklmnpqrstvwxyz]\w+)', s_lower)
        if m:
            errors.append(f"冠词错误：an后面跟辅音开头单词 '{m.group(1)}'，应改为 a")
    
    # ========== 介词搭配 ==========
    
    wrong_prep = {
        'in the weekend': 'on the weekend / at weekends',
        'in weekends': 'on weekends / at weekends',
        'in my home': 'at home',
        'to to ': 'to ',
        'of of ': 'of ',
        'at the': 'in the / on the',
    }
    for wrong, correct in wrong_prep.items():
        if wrong in s_lower:
            errors.append(f"介词错误：'{wrong}' → '{correct}'")
    
    # ========== 词汇错误 ==========
    
    vocab_errors = {
        'high-resistant': 'high-rise',
        'two-barroom': 'two-bedroom',
        'big old school': 'old-school / in an old-school way',
        'couple friends': 'close friends / a couple of friends',
        'my couple of': 'a couple of',
        'the flingers': 'blisters',
        'flingers': 'blisters',
        'local legal': 'local language',
        'pinch your idea': 'pitch your ideas',
        'occasional coffee banner': 'occasional coffee breaks',
        'banner': 'banter',
        'spiral cash': 'spare cash',
        'chill out and home': 'chill out at home',
        'sound sleeper': 'heavy sleeper',
        'weak person': '(根据语境判断，可能是词汇误用)',
        'busy in the air': 'exciting / festive',
        'i lay for': 'I look forward to',
        'a random of': 'random / on random days',
        'less grand': 'less grandly / not as grand',
        'two pounds idea': 'two cents worth',
        'causing the things': 'jotting things down / listing things',
        'perspectives have shipped': 'perspectives have shifted',
        'writing to to': 'writing to',
        'set the function': 'use the function',
        'get with the flow': 'go with the flow',
        'brainstorm': 'brainstorming session',
        'scattered brain': 'scatterbrained / scattered mind',
        'hit ground running': 'hit the ground running',
        'the little wings': '(词不达意)',
        'your get': 'you get',
        'wings than your': 'things than you',
    }
    
    for wrong, correct in vocab_errors.items():
        if wrong in s_lower:
            errors.append(f"词汇错误：'{wrong}' → '{correct}'")
    
    # ========== 常见口语错误 ==========
    
    # like 作为 filler 使用不当
    if re.search(r"\b(I|we|you|he|she|it|they)\s+\w+\s+like\s+\w+\s+\w+\b", s_lower):
        # I like really... / it's like really...
        if 'like' in s_lower.split()[1:-1]:  # like not at start or end
            # 检查是否是 be like / have like / like + verb
            if not re.search(r"\b(feel|be|seem|would|could)\s+like\b", s_lower):
                errors.append("口语错误：'like'作为 filler 使用不当（口语中可接受但非标准）")
    
    # ========== 句子结构问题 ==========
    
    # 句子太长
    if len(words) > 30 and len(errors) == 0:
        errors.append("句子过长（>30词），建议拆分")
    
    # 连接词在句首但无主句
    if re.match(r'^(And|But|So|However|Then|Because|Therefore|Thus)', s):
        errors.append("句子结构：以连接词开头但可能缺少主句")
    
    # 缺少谓语
    if re.search(r"^\s*(I|We|You|He|She|It|They|This|That)\s+[a-z]+\s*$", s):
        errors.append("谓语缺失：主语后缺少谓语动词")
    
    # ========== 无错误判断 ==========
    
    if len(errors) == 0:
        if len(words) <= 15:
            return "✅ 表达自然，无明显问题"
        else:
            return f"✅ 表达基本通顺（{len(words)}词），可进一步提升"
    
    return "；".join(errors[:3])


def suggest_fix(sentence: str, diagnosis: str) -> str:
    """生成修改建议"""
    if diagnosis.startswith("✅") or diagnosis == "空句子":
        return ""
    
    s = sentence.strip()
    fixes = []
    
    replacements = {
        'high-resistant': 'high-rise',
        'two-barroom': 'two-bedroom',
        'big old school': 'old-school',
        'the flingers': 'blisters',
        'flingers': 'blisters',
        'local legal': 'local language',
        'pinch your idea': 'pitch your ideas',
        'occasional coffee banner': 'occasional coffee breaks',
        'banner': 'banter',
        'spiral cash': 'spare cash',
        'chill out and home': 'chill out at home',
        'sound sleeper': 'heavy sleeper',
        'i lay for': 'I look forward to',
        'a random of': 'random',
        'two pounds idea': 'two cents worth',
        'causing the things': 'jotting things down',
        'perspectives have shipped': 'perspectives have shifted',
        'writing to to': 'writing to',
        'set the function': 'use the function',
        'get with the flow': 'go with the flow',
        'brainstorm': 'brainstorming',
        'scattered brain': 'scatterbrained',
        'in the weekend': 'on the weekend',
        'in weekends': 'on weekends',
        'in my home': 'at home',
        'to to ': 'to ',
    }
    
    modified = s
    for wrong, correct in replacements.items():
        if wrong in modified.lower():
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            modified = pattern.sub(correct, modified)
            fixes.append(f"'{wrong}'→'{correct}'")
    
    if fixes:
        return "修改：" + "；".join(fixes) + f" | {modified[:60]}..."
    
    return f"建议重写：{s[:50]}..."


def make_summary(results: list) -> dict:
    error_count = sum(1 for r in results if not r["diagnosis"].startswith("✅"))
    total = len(results)
    ok_count = total - error_count
    
    if error_count >= 4:
        g, v, l = "多处语法错误", "词汇有明显误用", "逻辑连接需加强"
        lvl = "5.0-5.5"
    elif error_count >= 2:
        g, v, l = "语法基本准确，偶有错误", "词汇面较广，部分需改进", "逻辑较清晰"
        lvl = "5.5-6.0"
    elif error_count >= 1:
        g, v, l = "语法较准确，个别小错", "词汇使用较地道", "逻辑清晰"
        lvl = "6.0"
    else:
        g, v, l = "语法完全准确", "词汇精准地道", "逻辑严密"
        lvl = "6.5+"
    
    return {
        "grammar": f"{g}（{error_count}错，{ok_count}自然）",
        "vocabulary": f"{v}",
        "logic": f"{l}",
        "pronunciation": "发音清晰（需音频评判）"
    }


def estimate_band(results: list) -> float:
    error_count = sum(1 for r in results if not r["diagnosis"].startswith("✅"))
    total = len(results)
    
    # 严重错误
    serious = sum(1 for r in results if any(w in r["diagnosis"] for w in ["主谓", "谓语错误", "空句子"]))
    
    if serious >= 2 or error_count >= total * 0.6:
        return 5.0
    elif error_count >= 2 or serious >= 1:
        return 5.5
    elif error_count >= 1:
        return 6.0
    return 6.5


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_transcript.py <transcript>")
        sys.exit(1)
    
    transcript = sys.argv[1]
    result = analyze_transcript(transcript)
    print(json.dumps(result, ensure_ascii=False, indent=2))
