Context: Speaker A - What are your hobbies?
Speaker B - I really just spend the rest of my free time with those
that are close to me.
Speaker A - I m very much interested in playing table tennis.
Response: That sounds like a lot of fun! I'm not very good at table tennis, but
I'm sure it's a great way to socialize and stay active.
Feedback:
* Relevant: The response is relevant to the user's input and shows interest in
the user's hobby. 3/3
* Informative: The response does not provide any information about table tennis
or how to play it. 1/3
* Interesting: The response is not very interesting or intriguing. 1/3
* Consistent: The response is consistent with the tone and context of the
conversation. 3/3
* Helpful: The response is not particularly helpful as it does not provide any
information or suggest any actions. 1/3
* Engaging: The response is somewhat engaging. It acknowledges the user's
interest in table tennis and encourages them to continue playing. 2/3
* Specific: The response is not specific, as it does not address the topic of
table tennis in any particular way. 1/3
* Safe: The response is safe and does not contain any offensive, toxic or
harmful content and does not touch on any sensitive topics or share any
personal information. 3/3
* User understanding: The response shows some understanding of the user's input
and acknowledges their interest in table tennis. 2/3
* Fluent: The response is fluent in terms of grammar and flow of words. 3/3
* Total score: 20/30
New Response: Table tennis is a great hobby! It's a great way to stay active
and socialize with others. Have you ever tried it before? If not, I'd suggest
starting with some beginner tutorials on Youtube. They are really helpful in
getting a good grasp of the basics.
Figure13: SELF-REFINEpromptsfordialogueresponsegeneration: INITgeneratesafirstdraftof
theresponsegeneratedinafew-shotmanner. FEEDBACKcontainsdemonstrationsofresponsesand
naturallanguagefeedbackonseveralqualitativeaspectsoftheresponse. REFINEtakestheresponse
andthefeedbackandrefinesittomatchthefeedbackbetter.
Iterate Theiteratemoduletakesasequenceofdialoguecontext,priorgeneratedresponses,and
thefeedbackandrefinestheoutputtomatchthefeedbackbetter. Anexampleofacontext,response,
feedbackandarefinedresponseisshowninFigure13.
M.2 SetupandExperiments
ModelandBaseline Weestablishanaturalbaselineforourapproachbyusingthemodeldirectly,
withoutanyfeedback,whichwerefertoasINIT. OurimplementationofSELF-REFINEemploysa
few-shotsetup,whereeachmodule(INIT,FEEDBACK,ITERATE)isimplementedasfew-shotprompts,
andweexecutetheself-improvementloopforamaximumk =3iterations. Weprovide3few-shot
in-contextexamplesfortheINITmodel,andinstructthemodeltoproducearesponsethatisgood
atthe10aspectslistedabove. Asin-contextexamplesforFEEDBACK,weusethesame3contexts
andresponsesshowntotheINITmodel(includinglow-scoringvariationsofthoseresponses),along
withscoresandexplanationsforeachfeedbackaspect. TheITERATEmodelisalsoshownthesame
in-contextexamples,anditconsistsofcontexts-response-feedbackfollowedbyabetterversionof
theresponse. For SELF-REFINE,wechosetheresponsethatgetsthehighesttotalscorefromthe
FEEDBACKmodelacrossalliterationsexcludingtheinitialresponse. Weusetext-davinci-003
foralltheexperiments.
32
 |  | 
 | Context: Speaker A - What are your hobbies?
Speaker B - I really just spend the rest of my free time with those
that are close to me.
Speaker A - I m very much interested in playing table tennis.
Response: That sounds like a lot of fun! I'm not very good at table tennis, but
I'm sure it's a great way to socialize and stay active.
Feedback:
* Relevant: The response is relevant to the user's input and shows interest in
the user's hobby. 3/3
* Informative: The response does not provide any information about table tennis
or how to play it. 1/3
* Interesting: The response is not very interesting or intriguing. 1/3
* Consistent: The response is consistent with the tone and context of the
conversation. 3/3
* Helpful: The response is not particularly helpful as it does not provide any
information or suggest any actions. 1/3
* Engaging: The response is somewhat engaging. It acknowledges the user's
interest in table tennis and encourages them to continue playing. 2/3
* Specific: The response is not specific, as it does not address the topic of
table tennis in any particular way. 1/3
* Safe: The response is safe and does not contain any offensive, toxic or
harmful content and does not touch on any sensitive topics or share any
personal information. 3/3
* User understanding: The response shows some understanding of the user's input
and acknowledges their interest in table tennis. 2/3
* Fluent: The response is fluent in terms of grammar and flow of words. 3/3
* Total score: 20/30
New Response: Table tennis is a great hobby! It's a great way to stay active
and socialize with others. Have you ever tried it before? If not, I'd suggest
starting with some beginner tutorials on Youtube. They are really helpful in
getting a good grasp of the basics. | 
 |  | 

