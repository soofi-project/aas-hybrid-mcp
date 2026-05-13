(a)Dialogue:x,y
t
(b)FEEDBACK fb (c)REFINE y
t+1
User: I am interested Engaging: Provides no Response (refined): That's
in playing Table information about table great to hear (...) ! It's
tennis. tennis or how to play it. a fun sport requiring
quick reflexes and good
Response: I'm sure User understanding: Lacks hand-eye coordination.
it's a great way to understanding of user's Have you played before, or
socialize, stay active needs and state of mind. are you looking to learn?
(d)Codeoptimization:x,y
t
(e)FEEDBACK fb (f)REFINE y
t+1
Generate sum of 1, ..., N This code is slow as Code (refined)
def sum(n): it uses brute force.
res = 0 A better approach is def sum_faster(n):
for i in range(n+1): to use the formula return (n*(n+1))//2
res += i ... (n(n+1))/2.
return res
Figure2: ExamplesofSELF-REFINE: aninitialoutput generatedbythebaseLLMandthenpassed
backtothesameLLMtoreceivefeedback tothesameLLMtorefinetheoutput . Thetoprow
illustratesthisfordialoggenerationwhereaninitialdialogueresponsecanbetransformedintoa
moreengagingonethatalsounderstandstheuserbyapplyingfeedback. Thebottomrowillustrates
thisforcodeoptimizationwherethecodeismademoreefficientbyapplyingfeedback.
Algorithm1SELF-REFINEalgorithm
Require: inputx,modelM,prompts{p ,p ,p },stopconditionstop(·)
gen fb refine
1: y 0 =M(p gen ∥x) ▷Initialgeneration(Eqn.1)
2: foriterationt∈0,1,...do
3: fb t =M(p fb ∥x∥y t ) ▷Feedback(Eqn.2)
4: ifstop(fb t ,t)then ▷Stopcondition
5: break
6: else
7: y t+1 =M(p refine ∥x∥y 0 ∥fb 0 ∥...∥y t ∥fb t ) ▷Refine(Eqn.4)
8: endif
9: endfor
10: returny t
Figure3: TheSELF-REFINEalgorithm. See(§2)foradiscussionofeachcomponent.
For example, in Figure 2(d), the model generates functionally correct code for the given input.
Here,p isatask-specificfew-shotprompt(orinstruction)foraninitialgeneration,and∥denotes
gen
concatenation. Thefew-shotpromptcontainsinput-outputpairs⟨x(k),y(k)⟩forthetask.2
FEEDBACK Next, SELF-REFINE uses the same model M to provide feedback fb t on its own
output,givenatask-specificpromptp forgeneratingfeedback:
fb
fb =M(p ∥x∥y ). (2)
t fb t
Intuitively,thefeedbackmayaddressmultipleaspectsoftheoutput. Forexample,incodeoptimiza-
tion,thefeedbackmightaddresstheefficiency,readability,andoverallqualityofthecode.
2Few-shotprompting(alsoreferredtoas“in-contextlearning”)providesamodelwithapromptconsistingof
kin-contextexamplesofthetargettask,eachintheformofinput-outputpairs⟨x ,y ⟩(Brownetal.,2020).
i i
3
User: I am interested
in playing Table
tennis.
Response: I'm sure
it's a great way to
socialize, stay active | Engaging: Provides no
information about table
tennis or how to play it.
User understanding: Lacks
understanding of user's
needs and state of mind. |  | 
 |  | Response (refined): That's
great to hear (...) ! It's
a fun sport requiring
quick reflexes and good
hand-eye coordination.
Have you played before, or
are you looking to learn? | 
 |  |  | 

 | User: I am interested
in playing Table
tennis.
Response: I'm sure
it's a great way to
socialize, stay active

 | 
 | This code is slow as
it uses brute force.
A better approach is
to use the formula
... (n(n+1))/2.
 | 

Generate sum of 1, ..., N
def sum(n):
res = 0
for i in range(n+1):
res += i
return res | 

 | Code (refined)
def sum_faster(n):
return (n*(n+1))//2

