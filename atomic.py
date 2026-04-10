from typing import Any, Dict, List, Set


SECTION_NAMES = [
    "subject_condition",
    "resource_condition",
    "constraint",
    "actions",
]


def clean(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_action_token(token: str) -> str:
    token = clean(token)
    token = token.strip("{}").strip()
    return token


def parse_section_set(text: str, section_name: str) -> Set[str]:
    text = clean(text)
    if not text:
        return set()

    if section_name == "actions":
        parts = text.replace(",", " ").split()
        return {normalize_action_token(part) for part in parts if normalize_action_token(part)}

    parts = [clean(part) for part in text.split(",")]
    return {part for part in parts if part}


def compare_section(student_text: str, gt_value: Any, section_name: str) -> Dict[str, Any]:
    student_set = parse_section_set(student_text, section_name)

    gt_values = gt_value if isinstance(gt_value, list) else [gt_value]
    gt_option_sets = [parse_section_set(value, section_name) for value in gt_values]

    if not gt_option_sets:
        gt_option_sets = [set()]

    for gt_set in gt_option_sets:
        if student_set == gt_set:
            return {
                "is_correct": True,
                "student_items": sorted(student_set),
                "ground_truth_items": sorted(gt_set),
                "all_ground_truth_options": [sorted(opt) for opt in gt_option_sets],
                "correct_items": sorted(student_set),
                "incorrect_items": [],
                "missing_items": [],
            }

    best_gt_set = max(gt_option_sets, key=lambda opt: len(student_set & opt))

    return {
        "is_correct": False,
        "student_items": sorted(student_set),
        "ground_truth_items": sorted(best_gt_set),
        "all_ground_truth_options": [sorted(opt) for opt in gt_option_sets],
        "correct_items": sorted(student_set & best_gt_set),
        "incorrect_items": sorted(student_set - best_gt_set),
        "missing_items": sorted(best_gt_set - student_set),
    }


def compare_atomic_rule(student_rule: Dict[str, str], ground_truth_rule: Dict[str, Any]) -> Dict[str, Any]:
    section_results: Dict[str, Any] = {}
    overall_correct = True

    for section in SECTION_NAMES:
        result = compare_section(
            student_rule.get(section, ""),
            ground_truth_rule.get(section, ""),
            section,
        )
        section_results[section] = result
        if not result["is_correct"]:
            overall_correct = False

    return {
        "is_correct": overall_correct,
        "sections": section_results,
    }


def format_atomic_feedback(result: Dict[str, Any]) -> str:
    lines: List[str] = [f'atomic_rule_correct: {result["is_correct"]}']

    for section in SECTION_NAMES:
        sec = result["sections"][section]
        lines.append("")
        lines.append(f"[{section}]")
        lines.append(f'is_correct: {sec["is_correct"]}')
        lines.append(f'student_items: {sec["student_items"]}')
        lines.append(f'ground_truth_items: {sec["ground_truth_items"]}')
        lines.append(f'all_ground_truth_options: {sec["all_ground_truth_options"]}')
        lines.append(f'correct_items: {sec["correct_items"]}')
        lines.append(f'incorrect_items: {sec["incorrect_items"]}')
        lines.append(f'missing_items: {sec["missing_items"]}')

    return "\n".join(lines)