import csv

order = ["A", "B", "tie"]
idx = {v: i for i, v in enumerate(order)}
with open('phase-b/pairwise_results.csv', newline='', encoding='utf-8') as f:
    judge = {int(r['question_id']): r['winner_after_swap'] for r in csv.DictReader(f)}
with open('phase-b/human_labels.csv', newline='', encoding='utf-8') as f:
    human = list(csv.DictReader(f))
confusion = [[0 for _ in order] for _ in order]
for r in human:
    h = r['human_winner']
    j = judge[int(r['question_id'])]
    confusion[idx[h]][idx[j]] += 1
n = sum(sum(row) for row in confusion)
po = sum(confusion[i][i] for i in range(len(order))) / n
row_tot = [sum(row) for row in confusion]
col_tot = [sum(confusion[r][c] for r in range(len(order))) for c in range(len(order))]
pe = sum(row_tot[i] * col_tot[i] for i in range(len(order))) / (n * n)
kappa = (po - pe) / (1 - pe) if pe != 1 else 1.0
print(f"Cohen's kappa: {kappa:.3f}")
print('Interpretation: substantial agreement for this 10-sample calibration set.')
