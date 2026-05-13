Table19: ApplicationA7. ExampleoutputofMiniWobChatononewebmanipulationtask“click-
button-sequence.”
Action AutoGen
g Initchat ExecutoragenttoAssistantAgent:
Wehaveanautonomouscomputercontrolagentthatcanperformatomicinstructionsspecifiedbynaturallanguagetocontrol
computers.Therearetwotypesofinstructionsitcanexecute.
First,giventheinstructionthatmatchestheregularexpression‘‘^type\s.{1,}$",itcantypealistofcharactersviathekeyboard.
Thisinstructionshouldspecifythetargetkeyboardinputfortheagenttotype.Beforethistypinginstruction,youshouldfirstlocate
thecursorbyclickingtheinputboxwithclickinstruction.
Second,giventheinstructionthatmatchestheregularexpression,‘‘^clickxpath\s.{1,}$",itcanclickanHTMLelement
withanxpaththatisvisibleonthewebpage.Thetargetofthisinstructionshouldbeavalidxpath.BelowistheHTMLcodeofthe
webpagewheretheagentshouldsolveatask.
1 <div id="wrap" data-wob_ref="2" data-wob_eps="e0">
2 <div id="query">Click button ONE, then click button TWO.</div>
3 <div id="area" data-wob_ref="3" data-wob_eps="e0">
4 <button id="subbtn" style="position:absolute; left:103px; top:87px" data-
wob_ref="4" data-wob_eps="e0">ONE</button>
5 <button id="subbtn2" style="position:absolute; left:44px; top:97px" data-
wob_ref="5" data-wob_eps="e0">TWO</button>
6 </div>
7 </div>
task:ClickbuttonONE,thenclickbuttonTWO.
plan:
1.Clickthebuttonwithxpath“//button[@id=‘subbtn’]”.
2.Clickthebuttonwithxpath“//button[@id=‘subbtn2’]”.
Currenttask:ClickbuttonONE,thenclickbuttonTWO.
plan:
(cid:240) ***************************************************************
AssistantAgenttoExecutoragent:
1.Clickthebuttonwithxpath“//button[@id=‘subbtn’]”.
2.Clickthebuttonwithxpath“//button[@id=‘subbtn2’]”.
***************************************************************
ExecutoragenttoAssistantAgent:
BelowistheHTMLcodeofthewebpagewheretheagentshouldsolveatask.
1 <div id="wrap" data-wob_ref="2" data-wob_eps="e0">
2 <div id="query">Click button ONE, then click button TWO.</div>
3 <div id="area" data-wob_ref="3" data-wob_eps="e0">
4 <button id="subbtn" style="position:absolute; left:103px; top:87px" data-
wob_ref="4" data-wob_eps="e0">ONE</button>
5 <button id="subbtn2" style="position:absolute; left:44px; top:97px" data-
wob_ref="5" data-wob_eps="e0">TWO</button>
6 </div>
7 </div>
Currenttask:ClickbuttonONE,thenclickbuttonTWO.
Hereisaplanyouarefollowingnow.
1.Clickthebuttonwithxpath“//button[@id=‘subbtn’]”.
2.Clickthebuttonwithxpath“//button[@id=‘subbtn2’]”.
Wehaveahistoryofinstructionsthathavebeenalreadyexecutedbytheautonomousagentsofar.
Noinstructionhasbeenexecutedyet.
Basedontheplanandthehistoryofinstructionsexecutedsofar,thefirstinstructionshouldbe‘
***************************************************************
AssistantAgenttoExecutoragent:
clickxpath//button[@id=‘subbtn’]
***************************************************************
ExecutoragenttoAssistantAgent:
Holdon,pleasewaitformynextinstruction.
***************************************************************
AssistantAgenttoExecutoragent:
Sure,I’llbeherewhenyou’rereadywithyournextinstruction.
***************************************************************
ExecutoragenttoAssistantAgent:
BelowistheHTMLcodeofthewebpagewheretheagentshouldsolveatask.
1 <div id="wrap" data-wob_ref="2" data-wob_eps="e0">
2 <div id="query">Click button ONE, then click button TWO.</div>
3 <div id="area" data-wob_ref="3" data-wob_eps="e0">
4 <button id="subbtn" style="position:absolute; left:103px; top:87px" data-
wob_ref="4" data-wob_eps="e0" data-tampered="e0">ONE</button>
5 <button id="subbtn2" style="position:absolute; left:44px; top:97px" data-
wob_ref="5" data-wob_eps="e0">TWO</button>
6 </div>
7 </div>
Currenttask:ClickbuttonONE,thenclickbuttonTWO.
Hereisaplanyouarefollowingnow.
1.Clickthebuttonwithxpath“//button[@id=‘subbtn’]”.
2.Clickthebuttonwithxpath“//button[@id=‘subbtn2’]”.
Wehaveahistoryofinstructionsthathavebeenalreadyexecutedbytheautonomousagentsofar.
1:clickxpath//button[@id=‘subbtn’]
Basedontheplanandthehistoryofinstructionsexecutedsofar,thenextproperinstructionshouldbe‘
***************************************************************
AssistantAgenttoExecutoragent:
clickxpath//button[@id=‘subbtn2’]
***************************************************************
ExecutoragenttoAssistantAgent:
SUCCESS!!!!
(cid:240) TERMINATE
43
1 <div id="wrap" data-wob_ref="2" data-wob_eps="e0">
2 <div id="query">Click button ONE, then click button TWO.</div>
3 <div id="area" data-wob_ref="3" data-wob_eps="e0">
4 <button id="subbtn" style="position:absolute; left:103px; top:87px" data-
wob_ref="4" data-wob_eps="e0">ONE</button>
5 <button id="subbtn2" style="position:absolute; left:44px; top:97px" data-
wob_ref="5" data-wob_eps="e0">TWO</button>
6 </div>
7 </div>

1 <div id="wrap" data-wob_ref="2" data-wob_eps="e0">
2 <div id="query">Click button ONE, then click button TWO.</div>
3 <div id="area" data-wob_ref="3" data-wob_eps="e0">
4 <button id="subbtn" style="position:absolute; left:103px; top:87px" data-
wob_ref="4" data-wob_eps="e0">ONE</button>
5 <button id="subbtn2" style="position:absolute; left:44px; top:97px" data-
wob_ref="5" data-wob_eps="e0">TWO</button>
6 </div>
7 </div>

1 <div id="wrap" data-wob_ref="2" data-wob_eps="e0">
2 <div id="query">Click button ONE, then click button TWO.</div>
3 <div id="area" data-wob_ref="3" data-wob_eps="e0">
4 <button id="subbtn" style="position:absolute; left:103px; top:87px" data-
wob_ref="4" data-wob_eps="e0" data-tampered="e0">ONE</button>
5 <button id="subbtn2" style="position:absolute; left:44px; top:97px" data-
wob_ref="5" data-wob_eps="e0">TWO</button>
6 </div>
7 </div>

