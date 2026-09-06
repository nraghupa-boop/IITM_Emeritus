from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from eval.custom_gemini_eval import GeminiDeepEvalLLM
from agent.orchestrator import UdaPlayOrchestrator

def execute_evaluation():
    eval_llm = GeminiDeepEvalLLM()
    orchestrator = UdaPlayOrchestrator()
    
    test_query = "Who developed FIFA 21?"
    result = orchestrator.route_and_execute(test_query)
    
    faithfulness = FaithfulnessMetric(
        threshold=0.7,
        model=eval_llm
    )
    
    completeness = GEval(
        name="Completeness",
        criteria="Determine if the actual output completely answers all parts of the input question.",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=eval_llm,
        threshold=0.7
    )

    correctness = GEval(
        name="Correctness",
        criteria="Determine if the actual output is factually aligned with the expected ground truth.",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        model=eval_llm,
        threshold=0.7
    )

    test_case = LLMTestCase(
        input=test_query,
        actual_output=result["final_response"],
        expected_output="FIFA 21 was developed by EA Vancouver and EA Romania.",
        retrieval_context=[result["context"]]
    )

    evaluate([test_case], [faithfulness, completeness, correctness])

if __name__ == "__main__":
    execute_evaluation()
