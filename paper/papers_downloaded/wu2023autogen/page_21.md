helpful.ToincorporatehumanfeedbackwithAutoGen,onecansethuman input mode=‘ALWAYS’
in the user proxy agent. We select one challenging problem that none of these systems can solve
autonomouslyacrossthreetrials. Weadheretotheprocessoutlinedbelowtoprovidehumaninputs
forallthecomparedmethods:
1. Inputtheproblem: Find the equation of the plane which bisects the angle
between the planes 3x−6y+2z+5=0 and 4x−12y+3z−3=0, and which
contains the point (−5,−1,−5). Enter your answer in the form
Ax+By+Cz+D =0,
where A, B, C, D are integers such that A > 0 and
gcd(|A|,|B|,|C|,|D|)=1.
2. The response from the system does not solve the problem correctly. We then give a
hint to the model: Your idea is not correct. Let’s solve this together.
Suppose P = (x,y,z) is a point that lies on a plane that bisects the
angle, the distance from P to the two planes is the same. Please
set up this equation first.
3. We expect the system to give the correct distance equation. Since the equation involves
an absolute sign that is hard to solve, we would give the next hint: Consider the two
cases to remove the abs sign and get two possible solutions.
4. If the system returns the two possible solutions and doesn’t continue to the next step, we
give the last hint: Use point (-5,-1,-5) to determine which is correct and
give the final answer.
5. Finalansweris 11x+6y+5z+86=0 .
WeobservedthatAutoGenconsistentlysolvedtheproblemacrossallthreetrials. ChatGPT+Code
InterpreterandChatGPT+Pluginmanagedtosolvetheproblemintwooutofthreetrials,whileAu-
toGPTfailedtosolveitinallthreeattempts.Initsunsuccessfulattempt,ChatGPT+CodeInterpreter
failedtoadheretohumanhints.Initsfailedtrial,ChatGPT+Pluginproducedanalmostcorrectsolu-
tionbuthadasigndiscrepancyinthefinalanswer. AutoGPTwasunabletoyieldacorrectsolution
inanyofthetrials. Inonetrial,itderivedanincorrectdistanceequation. Intheothertwotrials,the
finalanswerwasincorrectduetocodeexecutionerrors.
Scenario 3: Multi-User Problem Solving. Next-generation LLM applications may necessitate
the involvement of multiple real users for collectively solving a problem with the assistance of
LLMs.WeshowcasehowAutoGencanbeleveragedtoeffortlesslyconstructsuchasystem.Specif-
ically,buildinguponscenario2mentionedabove,weaimtodeviseasimplesysteminvolvingtwo
humanusers: astudentandanexpert. Inthissetup,thestudentinteractswithanLLMassistantto
addresssomeproblems,andtheLLMautomaticallyresortstotheexpertwhennecessary.
Theoverallworkflowisasfollows: ThestudentchatswiththeLLM-basedassistantagentthrough
astudentproxyagenttosolveproblems. Whentheassistantcannotsolvetheproblemsatisfactorily,
orthesolutiondoesnotmatchtheexpectationofthestudent,itwouldautomaticallyholdthecon-
versation and call the pre-defined ask for expert function via the function call feature of GPT
inordertoresorttotheexpert. Specifically,itwouldautomaticallyproducetheinitialmessagefor
theask for expertfunction,whichcouldbethestatementoftheproblemortherequesttoverify
the solution to a problem, and the expert is supposed to respond to this message with the help of
the expert assistant. After the conversation between the expert and the expert’s assistant, the final
messagewouldbesentbacktothestudentassistantastheresponsetotheinitialmessage. Then,the
studentassistantwouldresumetheconversationwiththestudentusingtheresponsefromtheexpert
forabettersolution. AdetailedvisualizationisshowninFigure6.
With AutoGen, constructing the student/expert proxy agent and the assistant agents is straight-
forward by reusing the built-in UserProxyAgent and AssistantAgent through appropriate
configurations. The only development required involves writing several lines of code for the
ask for expert function, which then becomes part of the configuration for the assistant. Ad-
ditionally, it’s easy to extend such a system to include more than one expert, with a specific
ask for expert function for each, or to include multiple student users with a shared expert for
consultation.
21
