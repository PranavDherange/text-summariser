from rouge import Rouge

def get_rouge_scores(hypothesis, reference):
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference, avg=True)
    return scores

# Example usage:
hyp = "the cat was found under the bed"
ref = "the cat was hiding under the bed"
scores = get_rouge_scores(hyp, ref)
print(scores)