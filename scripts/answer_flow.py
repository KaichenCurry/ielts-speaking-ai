#!/usr/bin/env python3
"""
雅思口语答题状态机
管理 Part1 → Part2 → Part3 → 完成 的完整流程
"""
import json
import sys
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict

class Stage(Enum):
    IDLE = "idle"
    PART1 = "part1"      # 等待Part1答题
    PART1_ANSWERING = "part1_answering"  # 等待语音
    PART2 = "part2"
    PART2_ANSWERING = "part2_answering"
    PART3 = "part3"
    PART3_ANSWERING = "part3_answering"
    DONE = "done"

@dataclass
class AnswerRecord:
    """单题答题记录"""
    question: str
    answer: str = ""
    band: float = 0.0
    evaluation: str = ""
    error_types: List[str] = field(default_factory=list)  # 语法/词汇/时态/逻辑/思路

@dataclass
class SessionState:
    """会话状态"""
    student_id: str
    student_nickname: str
    test_num: int
    topic_short_id: str
    topic_en: str
    category: str
    
    # Part数据
    part1_questions: List[str] = field(default_factory=list)
    part2_topic: str = ""
    part2_should_say: List[str] = field(default_factory=list)
    part3_questions: List[str] = field(default_factory=list)
    
    # 当前进度
    stage: Stage = Stage.IDLE
    current_part1_idx: int = 0
    current_part3_idx: int = 0
    
    # 答题记录
    part1_answers: List[AnswerRecord] = field(default_factory=list)
    part2_answer: Optional[AnswerRecord] = None
    part3_answers: List[AnswerRecord] = field(default_factory=list)
    
    # 最终结果（None表示未评分）
    part1_band: Optional[float] = None
    part2_band: Optional[float] = None
    part3_band: Optional[float] = None
    overall_band: float = 0.0
    
    def get_current_part1_question(self) -> Optional[str]:
        """获取当前Part1问题"""
        if 0 <= self.current_part1_idx < len(self.part1_questions):
            return self.part1_questions[self.current_part1_idx]
        return None
    
    def get_current_part3_question(self) -> Optional[str]:
        """获取当前Part3问题"""
        if 0 <= self.current_part3_idx < len(self.part3_questions):
            return self.part3_questions[self.current_part3_idx]
        return None
    
    def has_more_part1(self) -> bool:
        return self.current_part1_idx < len(self.part1_questions)
    
    def has_more_part3(self) -> bool:
        return self.current_part3_idx < len(self.part3_questions)
    
    def next_part1(self):
        self.current_part1_idx += 1
    
    def next_part3(self):
        self.current_part3_idx += 1
    
    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "student_nickname": self.student_nickname,
            "test_num": self.test_num,
            "topic_short_id": self.topic_short_id,
            "topic_en": self.topic_en,
            "category": self.category,
            "stage": self.stage.value,
            "part1_answers": [
                {"q": a.question, "a": a.answer, "band": a.band, "eval": a.evaluation}
                for a in self.part1_answers
            ],
            "part2_answer": {
                "q": self.part2_answer.question,
                "a": self.part2_answer.answer,
                "band": self.part2_answer.band,
                "eval": self.part2_answer.evaluation
            } if self.part2_answer else None,
            "part3_answers": [
                {"q": a.question, "a": a.answer, "band": a.band, "eval": a.evaluation}
                for a in self.part3_answers
            ],
            "overall_band": self.overall_band
        }


class AnswerFlow:
    """答题流程控制器"""
    
    def __init__(self):
        # 内存中的会话状态 {student_id: SessionState}
        self.sessions: Dict[str, SessionState] = {}
    
    def start_session(self, student_id: str, student_nickname: str, 
                     test_num: int, topic_short_id: str, topic_en: str,
                     category: str, part1_questions: List[str],
                     part2_topic: str, part2_should_say: List[str],
                     part3_questions: List[str]) -> SessionState:
        """开始新答题会话"""
        state = SessionState(
            student_id=student_id,
            student_nickname=student_nickname,
            test_num=test_num,
            topic_short_id=topic_short_id,
            topic_en=topic_en,
            category=category,
            part1_questions=part1_questions,
            part2_topic=part2_topic,
            part2_should_say=part2_should_say,
            part3_questions=part3_questions,
            stage=Stage.PART1,
            part1_answers=[AnswerRecord(q) for q in part1_questions],
            part3_answers=[AnswerRecord(q) for q in part3_questions]
        )
        self.sessions[student_id] = state
        return state
    
    def get_session(self, student_id: str) -> Optional[SessionState]:
        return self.sessions.get(student_id)
    
    def record_answer(self, student_id: str, answer: str, 
                     band: float = None, evaluation: str = None, 
                     error_types: List[str] = None,
                     skip_evaluation: bool = False) -> dict:
        """
        记录学生回答，并根据当前状态返回下一步动作
        
        如果 skip_evaluation=True，则只记录音频识别结果，不做AI评分
        适用于：录音后立即发下一题，评分后续异步进行
        """
        state = self.sessions.get(student_id)
        if not state:
            return {"error": "No active session"}
        
        # 获取当前问题
        question = self._get_current_question(state)
        
        # 如果跳过评分，只记录文本
        if skip_evaluation:
            record = AnswerRecord(
                question=question,
                answer=answer,
                band=0.0,
                evaluation="",
                error_types=[]
            )
        else:
            record = AnswerRecord(
                question=question,
                answer=answer,
                band=band or 0.0,
                evaluation=evaluation or "",
                error_types=error_types or []
            )
        
        if state.stage == Stage.PART1_ANSWERING:
            state.part1_answers[state.current_part1_idx] = record
            # 递增索引后检查是否还有下一题
            state.next_part1()
            if state.current_part1_idx < len(state.part1_questions):
                return self._next_part1(state)
            else:
                return self._transition_to_part2(state)
        
        elif state.stage == Stage.PART2_ANSWERING:
            state.part2_answer = record
            return self._transition_to_part3(state)
        
        elif state.stage == Stage.PART3_ANSWERING:
            state.part3_answers[state.current_part3_idx] = record
            # 递增索引后检查是否还有下一题
            state.next_part3()
            if state.current_part3_idx < len(state.part3_questions):
                return self._next_part3(state)
            else:
                return self._transition_to_done(state)
        
        return {"error": "Invalid state"}
    
    def update_evaluation(self, student_id: str, part: str, idx: int,
                        band: float, evaluation: str, error_types: List[str]) -> dict:
        """
        后续更新评分结果（异步评分完成后调用）
        part: 'part1', 'part2', 'part3'
        idx: Part1/Part3的题目索引，Part2传0
        """
        state = self.sessions.get(student_id)
        if not state:
            return {"error": "No active session"}
        
        if part == 'part1' and 0 <= idx < len(state.part1_answers):
            state.part1_answers[idx].band = band
            state.part1_answers[idx].evaluation = evaluation
            state.part1_answers[idx].error_types = error_types
        elif part == 'part2':
            if state.part2_answer:
                state.part2_answer.band = band
                state.part2_answer.evaluation = evaluation
                state.part2_answer.error_types = error_types
        elif part == 'part3' and 0 <= idx < len(state.part3_answers):
            state.part3_answers[idx].band = band
            state.part3_answers[idx].evaluation = evaluation
            state.part3_answers[idx].error_types = error_types
        
        return {"ok": True}
    
    def _get_current_question(self, state: SessionState) -> str:
        if state.stage in [Stage.PART1, Stage.PART1_ANSWERING]:
            return state.part1_questions[state.current_part1_idx]
        elif state.stage == Stage.PART2_ANSWERING:
            return state.part2_topic
        elif state.stage in [Stage.PART3, Stage.PART3_ANSWERING]:
            return state.part3_questions[state.current_part3_idx]
        return ""
    
    def _next_part1(self, state: SessionState) -> dict:
        """发送下一道Part1"""
        state.stage = Stage.PART1_ANSWERING
        q = state.get_current_part1_question()
        return {
            "action": "ask",
            "stage": "part1_answering",
            "question": q,
            "message": f"📝 Part 1 第 {state.current_part1_idx + 1} 题：\n\n{q}\n\n@学生 请录音回答"
        }
    
    def _next_part3(self, state: SessionState) -> dict:
        """发送下一道Part3"""
        state.stage = Stage.PART3_ANSWERING
        q = state.get_current_part3_question()
        return {
            "action": "ask",
            "stage": "part3_answering",
            "question": q,
            "message": f"📝 Part 3 第 {state.current_part3_idx + 1} 题：\n\n{q}\n\n@学生 请录音回答"
        }
    
    def _transition_to_part2(self, state: SessionState) -> dict:
        """Part1完成，切换到Part2"""
        state.stage = Stage.PART2_ANSWERING
        part2_card = f"📋 **Part 2 题卡：**\n\n{state.part2_topic}\n\n**You should say:**\n"
        for i, point in enumerate(state.part2_should_say, 1):
            part2_card += f"\n{i}. {point}"
        
        return {
            "action": "ask",
            "stage": "part2_answering",
            "question": state.part2_topic,
            "card": part2_card,
            "message": f"{part2_card}\n\n@学生 准备好后请发语音"
        }
    
    def _transition_to_part3(self, state: SessionState) -> dict:
        """Part2完成，切换到Part3"""
        state.stage = Stage.PART3_ANSWERING
        state.current_part3_idx = 0
        
        if state.part3_questions:
            q = state.part3_questions[0]
            return {
                "action": "ask",
                "stage": "part3_answering",
                "question": q,
                "message": f"📝 Part 3 第 1 题：\n\n{q}\n\n@学生 请录音回答"
            }
        else:
            # 没有Part3，直接结束
            return self._transition_to_done(state)
    
    def _transition_to_done(self, state: SessionState) -> dict:
        """全部完成，汇总结果"""
        state.stage = Stage.DONE
        
        # 计算平均Band
        if state.part1_answers:
            state.part1_band = sum(a.band for a in state.part1_answers) / len(state.part1_answers)
        if state.part2_answer:
            state.part2_band = state.part2_answer.band
        if state.part3_answers:
            state.part3_band = sum(a.band for a in state.part3_answers) / len(state.part3_answers)
        
        # 综合Band = Part1×30% + (Part2×40% + Part3×60%)×70%
        # 公式说明：
        #   Part2_3 合成 = Part2×0.4 + Part3×0.6
        #   Overall = Part1×0.3 + Part2_3×0.7
        if state.part1_band is not None and state.part2_band and state.part3_band is not None:
            p2_3_combined = state.part2_band * 0.4 + state.part3_band * 0.6
            state.overall_band = state.part1_band * 0.3 + p2_3_combined * 0.7
        elif state.part2_band and state.part3_band is not None:
            p2_3_combined = state.part2_band * 0.4 + state.part3_band * 0.6
            state.overall_band = p2_3_combined
        elif state.part2_band:
            state.overall_band = state.part2_band
        elif state.part3_band is not None:
            state.overall_band = state.part3_band
        elif state.part1_band is not None:
            state.overall_band = state.part1_band
        
        return {
            "action": "done",
            "stage": "done",
            "overall_band": round(state.overall_band, 1),
            "summary": self._generate_summary(state)
        }
    
    def _generate_summary(self, state: SessionState) -> str:
        """生成汇总报告"""
        lines = [
            f"🏆 **答题完成 | {state.student_nickname}**",
            "",
            f"📌 题目：{state.topic_short_id} | Test {state.test_num:02d}",
            "",
            "═" * 20,
            "📊 **Band Score**",
            "═" * 20,
        ]
        
        if state.part1_band:
            lines.append(f"Part 1：{round(state.part1_band, 1)}")
        if state.part2_band:
            lines.append(f"Part 2：{round(state.part2_band, 1)}")
        if state.part3_band:
            lines.append(f"Part 3：{round(state.part3_band, 1)}")
        
        lines.append("")
        lines.append(f"⭐ **综合Band：{round(state.overall_band, 1)} / 9.0**")
        
        return "\n".join(lines)
    
    def get_next_ask(self, student_id: str) -> Optional[dict]:
        """获取下一题（用于首次调用）"""
        state = self.sessions.get(student_id)
        if not state:
            return None
        
        if state.stage == Stage.PART1:
            return self._next_part1(state)
        elif state.stage == Stage.PART2:
            return self._transition_to_part2(state)
        elif state.stage == Stage.PART3:
            return self._transition_to_part3(state)
        
        return None
    
    def end_session(self, student_id: str):
        """结束会话"""
        if student_id in self.sessions:
            del self.sessions[student_id]


# 全局实例
_flow = AnswerFlow()

def start_answer_session(student_id: str, student_nickname: str, 
                        test_num: int, topic_short_id: str, topic_en: str,
                        category: str, part1_questions: List[str],
                        part2_topic: str, part2_should_say: List[str],
                        part3_questions: List[str]) -> dict:
    """开始答题会话"""
    state = _flow.start_session(
        student_id, student_nickname, test_num, topic_short_id,
        topic_en, category, part1_questions, part2_topic,
        part2_should_say, part3_questions
    )
    return _flow.get_next_ask(student_id)

def record_student_answer(student_id: str, answer: str, 
                         band: float = None, evaluation: str = None,
                         error_types: List[str] = None,
                         skip_evaluation: bool = False) -> dict:
    """记录学生回答
    
    Args:
        skip_evaluation: True时录音后立即发下一题，评分后续异步进行
    """
    return _flow.record_answer(student_id, answer, band, evaluation, 
                               error_types, skip_evaluation)

def update_answer_evaluation(student_id: str, part: str, idx: int,
                            band: float, evaluation: str, 
                            error_types: List[str]) -> dict:
    """后续更新评分结果（异步评分完成后调用）"""
    return _flow.update_evaluation(student_id, part, idx, band, evaluation, error_types)

def get_session_state(student_id: str) -> Optional[SessionState]:
    return _flow.get_session(student_id)

def end_answer_session(student_id: str):
    _flow.end_session(student_id)


if __name__ == "__main__":
    # 测试
    result = start_answer_session(
        student_id="test123",
        student_nickname="测试学生",
        test_num=48,
        topic_short_id="社交媒体趣事",
        topic_en="Describe an interesting story on social media",
        category="事件类",
        part1_questions=["Do you use social media?", "What apps do you use?"],
        part2_topic="Describe an interesting story on social media",
        part2_should_say=["what it was", "when it happened", "why it was interesting"],
        part3_questions=["How does social media affect communication?", "Is it good or bad?"]
    )
    print("启动会话:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n记录回答:")
    result = record_student_answer(
        student_id="test123",
        answer="Yes I use social media every day...",
        band=6.0,
        evaluation="语法正确，时态准确",
        error_types=["词汇"]
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
