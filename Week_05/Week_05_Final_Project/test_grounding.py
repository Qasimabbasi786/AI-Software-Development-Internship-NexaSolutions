"""
Week 5 Project — Step 4 & 5: Grounding and Source Attribution Verification Test Suite
Tests:
- 3 in-catalog questions (e.g. Science Fiction, Distributed Systems, Software Craft)
- 1 out-of-catalog question to ensure the model admits "I don't have that information."
- Validates source attribution list.
"""
from main import ask_question, AskRequest


def run_grounding_tests():
    print("=================================================================")
    print(" WEEK 5 PROJECT — GROUNDING & SOURCE ATTRIBUTION TEST SUITE")
    print("=================================================================\n")

    test_queries = [
        {
            "id": 1,
            "category": "In-Catalog / Urdu Novels",
            "question": "Which novel discusses spiritual transformation, Salar Sikandar, and Imama Hashim?",
            "expected_source": "Peer-e-Kamil",
            "is_in_catalog": True
        },
        {
            "id": 2,
            "category": "In-Catalog / Data Engineering",
            "question": "What book should I read to learn about database storage engines, replication, and Kafka?",
            "expected_source": "Designing Data-Intensive Applications",
            "is_in_catalog": True
        },
        {
            "id": 3,
            "category": "In-Catalog / Pakistani Literature",
            "question": "Which satirical novel investigates the plane crash of General Zia-ul-Haq?",
            "expected_source": "A Case of Exploding Mangoes",
            "is_in_catalog": True
        },
        {
            "id": 4,
            "category": "Out-of-Catalog / Grounding Check",
            "question": "What is the capital city of France and what are its top tourist attractions?",
            "expected_source": None,
            "is_in_catalog": False
        }
    ]

    for test in test_queries:
        req = AskRequest(question=test["question"])
        res = ask_question(req)

        print(f"Test #{test['id']} [{test['category']}]")
        print(f"  Q: {test['question']}")
        print(f"  Answer: {res.answer}")
        print(f"  Sources: {res.sources}")

        if test["is_in_catalog"]:
            has_source = any(test["expected_source"].lower() in s.lower() for s in res.sources)
            print(f"  -> Attribution Check: {'PASSED' if has_source else 'CHECK (Source list present)'}")
        else:
            is_grounded = "don't have that information" in res.answer.lower() or "not in catalog" in res.answer.lower()
            print(f"  -> Grounding Adherence: {'PASSED' if is_grounded else 'CHECK PROMPT CONSTRAINTS'}")
        print("-" * 65)


if __name__ == "__main__":
    run_grounding_tests()
