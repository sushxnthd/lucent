# Open Research Questions

These are the questions Lucent should answer in roughly this order.

## Signal existence

1. Does any short-video representation predict paired psychomotor performance on unseen participants?
2. Is the effect stronger for person-relative change than for absolute cross-person prediction?
3. Which target is most recoverable: median reaction time, lapse-like events, subjective sleepiness, or another state variable?

## Temporal value

4. Does full video beat a matched static frame?
5. How quickly does performance saturate as the observation window grows from 1 to 3 to 5 to 10+ seconds?
6. Which temporal cues matter after ablation: eyelid dynamics, blink timing, gaze stability, head motion, or learned features?

## Shortcut resistance

7. How much apparent performance disappears when random splits are replaced with participant-held-out splits?
8. Can participant identity or device identity be decoded from the learned representation?
9. Does the model still add information after controlling for sleep history and time of day?

## Robustness

10. Which shifts break the signal first: device, lighting, pose, glasses, compression, or session separation?
11. Does predictive uncertainty increase on those shifts?
12. Is there a bounded operating regime that can be stated honestly and reproduced?

## Personalization

13. How many personal-baseline observations are needed before within-person prediction materially improves?
14. Can a hybrid system perform useful cold-start prediction and then adapt safely over time?

## Replication

15. Does a frozen pipeline reproduce on a completely fresh cohort?
16. If not, which part fails first: representation, target, collection protocol, or generalization assumption?

## Decision rule

Lucent should not optimize for the largest number of positive findings.

It should optimize for the smallest claim that survives the strongest reasonable attempt to falsify it.
