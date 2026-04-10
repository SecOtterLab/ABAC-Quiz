from abac_logic.rule import RuleManager
from abac_logic.myabac import parse_abac_file
from abac_logic.acl_tools import generate_acl, compare_acl_sets


def evaluate_rules(rule_list, gt_acl_list, attribute_data_file):
    feedback_list = []

    user_mgr, res_mgr, _ = parse_abac_file(attribute_data_file)

    for i, rule_string in enumerate(rule_list):
        try:
            acl1 = gt_acl_list[i]

            rule_mgr = RuleManager()
            rule_mgr.parse_rule(rule_string)

            acl2 = generate_acl(user_mgr, res_mgr, rule_mgr)

            stats_text, lines, complete_match, _ = compare_acl_sets(acl1, acl2)
            feedback = stats_text + "\n" + "\n".join(lines)
            feedback_list.append(feedback)

        except Exception as e:
            feedback_list.append(f"Error evaluating rule: {rule_string} -> {e}")

    return feedback_list


ACL1 = {
    "oncNurse1, oncPat1HR, modify",
    "carNurse1, carPat1HR, modify",
    "oncNurse2, oncPat2HR, modify",
    "oncPat2, oncPat1HR, modify",
    "carPat2, carPat1HR, modify",
    "carNurse2, carPat2HR, modify",
    "oncPat2, oncPat2HR, modify",
    "carPat1, carPat2HR, modify",
    "carPat1, carPat1HR, modify",
    "oncPat1, oncPat2HR, modify",
    "carNurse2, carPat1HR, modify",
    "carPat2, carPat2HR, modify",
    "oncNurse1, oncPat2HR, modify",
    "oncPat1, oncPat1HR, modify",
    "carNurse1, carPat2HR, modify",
    "oncNurse2, oncPat1HR, modify",
}

ACL2 = {
    "anesDoc1, oncPat1HR, modify",
    "oncDoc4, oncPat2HR, modify",
    "anesDoc1, carPat1HR, modify",
    "carDoc1, carPat1HR, modify",
    "oncDoc3, oncPat2HR, modify",
    "carDoc2, carPat2HR, modify",
    "oncDoc1, oncPat1HR, modify",
    "oncDoc1, oncPat2HR, modify",
    "oncDoc2, oncPat1HR, modify",
}

ACL3 = {
    "oncPat2, oncPat2HR, modify",
    "carPat2, carPat2HR, modify",
    "carPat1, carPat1HR, modify",
    "oncPat1, oncPat1HR, modify",
}

ACL4 = {
    "oncAgent2, oncPat2HR, modify",
    "carAgent1, carPat2HR, modify",
    "carAgent1, carPat2HR, read",
    "oncAgent2, oncPat2HR, read",
    "oncAgent1, oncPat2HR, read",
    "carAgent2, carPat2HR, read",
    "oncAgent1, oncPat2HR, modify",
    "carAgent2, carPat2HR, modify",
}

ACL5 = {
    "oncDoc2, oncPat1oncItem, modify",
    "oncDoc4, oncPat2oncItem, modify",
    "carDoc2, carPat2carItem, modify",
    "oncDoc3, oncPat2oncItem, modify",
    "oncDoc1, oncPat2oncItem, modify",
    "oncDoc1, oncPat1oncItem, modify",
    "carDoc1, carPat1carItem, modify",
}

ACL6 = {
    "doc2, carPat2carItem, delete",
    "oncNurse2, oncPat1nursingItem, delete",
    "carAgent1, carPat2noteItem, read",
    "oncNurse1, oncPat2nursingItem, read",
    "carNurse2, carPat2nursingItem, delete",
    "doc1, oncPat2oncItem, read",
    "carNurse2, carPat2nursingItem, read",
    "oncNurse1, oncPat2nursingItem, delete",
    "carNurse1, carPat1nursingItem, read",
    "carPat1, carPat1noteItem, delete",
    "carDoc2, carPat1carItem, delete",
    "doc2, carPat2carItem, read",
    "oncAgent1, oncPat2noteItem, delete",
    "carAgent1, carPat2noteItem, delete",
    "carDoc2, carPat1carItem, read",
    "oncPat1, oncPat1noteItem, delete",
    "oncAgent1, oncPat2noteItem, read",
    "oncDoc1, oncPat1oncItem, delete",
    "carNurse1, carPat1nursingItem, delete",
    "carPat1, carPat1noteItem, read",
    "oncDoc1, oncPat1oncItem, read",
    "doc1, oncPat2oncItem, delete",
    "oncPat1, oncPat1noteItem, read",
    "oncNurse2, oncPat1nursingItem, read",
}

GT_ACL_LIST = [ACL1, ACL2, ACL3, ACL4, ACL5, ACL6]


GT_RULE_LIST = [
    "rule(; type [ {HR}; ward = ward; {modify})",
    "rule(; type [ {HR}; teams ] treatingTeam; {modify})",
    "rule(; type [ {HR}; uid = patient; {modify})",
    "rule(; type [ {HR}; agentFor ] patient; {read modify})",
    "rule(; type [ {HRitem}; teams ] treatingTeam, specialties > topics; {modify})",
    "rule(; type [] {HRitem}; uid = author; {read delete})",
]


def print_generated_acl(rule_string, attribute_data_file):
    user_mgr, res_mgr, _ = parse_abac_file(attribute_data_file)

    rule_mgr = RuleManager()
    rule_mgr.parse_rule(rule_string)

    acl = generate_acl(user_mgr, res_mgr, rule_mgr)
    return acl


def main():
    attribute_data_file = "healthcare-data/healthcare-attribute-data.txt"

    print("=" * 80)
    print("GROUND TRUTH RULES")
    print("=" * 80)
    for i, rule in enumerate(GT_RULE_LIST, start=1):
        print(f"{i}. {rule}")

    print("\n" + "=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)

    feedback_list = evaluate_rules(GT_RULE_LIST, GT_ACL_LIST, attribute_data_file)

    for i, feedback in enumerate(feedback_list, start=1):
        print("\n" + "-" * 80)
        print(f"QUESTION {i}")
        print("-" * 80)
        print("RULE:")
        print(GT_RULE_LIST[i - 1])
        print("\nFEEDBACK:")
        print(feedback)

    print("\n" + "=" * 80)
    print("OPTIONAL DEBUG: GENERATED ACL COUNTS")
    print("=" * 80)

    for i, rule in enumerate(GT_RULE_LIST, start=1):
        try:
            acl = print_generated_acl(rule, attribute_data_file)
            print(f"Question {i}: generated {len(acl)} permissions, expected {len(GT_ACL_LIST[i - 1])}")
        except Exception as e:
            print(f"Question {i}: parse/generate error -> {e}")


if __name__ == "__main__":
    main()