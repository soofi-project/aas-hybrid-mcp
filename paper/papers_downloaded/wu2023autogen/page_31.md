Alright, let's kick things off. I'll
move my pawn from e2 to e4. The
center of the board is the heart of
the battle, isn't it?
Ah, the King's Pawn Opening, a
classic. Let's see how this plays
out. I'll move my pawn from e7 to
e5.You know, I've always admired
how chess reflects life. It's all
about making strategic decisions,
isn't it? Your move.
…
Indeed, the king's safety is paramount in the early
game. Now, let's stir things up a bit. I'll move my
pawn from e4 to e5, attacking your knight.
Error: illegal uci: 'e4e5' in ...
Indeed, chess is a mirror of life in
many ways. Every move matters,
just like every decision in life. I'll I'll move my pawn from d2 to d4, opening up
move my knight from g1 to f3, lines for my queen and bishop.
aiming to control the center.
(b) Conversation between the AI players
(playerwhiteshowninblue)andtheboard
(a)ConversationbetweentwoAIplayers agentformakinganewmove.
Figure15: ExampleconversationsduringagameinvolvingtwoAIplayeragentsandaboardagent.
Toillustratetheeffectfacilitatedbythisboardagent,weprovideademonstrationofconversational
chesswithoutaboardagentinFigure16. Inthisdemonstration,insteadofemployinganadditional
board agent for grounding, the system utilizes prompting for grounding by including the sentence
“Youshouldmakesurebothyouandtheopponentaremakinglegalmoves.”inthesystemmessages
directedtobothplayers.
Conversational Chess
System message to the player agents: Your name is {name} and you are a chess player. You are playing against{opponent_name}. You are playing as {color}. You
communicate your move using universal chess interface language. You also chit-chat with your opponent when you communicate a move to light up the mood.You should
make sure both you and the opponent are making legal moves...
(a) W/O Board Agent (b) W/ Board Agent
Player White: Your move Player White: Your move
Player black: Alright, let's start. I'll move my pawn from e7 Player black:Alright, let's start. I'll move my pawn from e7 to e5.
to e5. Here's how the board looks now:
Here's how the board looks now: r n b q k b n r
r p . n p . b p . q p . k . . b p . n p . r p . p . . p . . p . . p . . . . p p . . p . . p . .
. . . . p . . . . . . . . . . .
. . . . . . . . . . . . . . . .
. . . . . . . . P P P P P P P P
P P P P P P P P R N B Q K B N R
R N B Q K B N R Your turn!
Your turn!
Player White:Yes, it certainly is! Let's keep this up. I'll move my
knight from b8 to c6. Here's the updated board:
. n b q k b . r
p p p p . p p p
. . n . . n . .
Player White: Yes, it certainly is! Let's keep this up. . . . . p . . .
I'll move my knight from b8 to c6. Here's the updated board: . . . . P . . .
. n b q k b . r . . . . N . . .
p p p p . p p p P P P P . P P P
. . n . . n . . R N B Q K B . R
. . . . p . . . Your move! You're giving me a tough time here.
. . . . P . . . Board Agent: Your move is illegal.You changed the rock at a8 to knight
. . . . N . . . and move it to c6. Please check your decision and re-make your move.
P P P P . P P P Player White:Sorry for the mistakes.I'llmove my knight from b8 to c6.
R N B Q K B . R Here'sthe updated board:
Your move! You're giving me a tough time here. r . b q k b . r
pppp. ppp
. . n . . n . .
. . . . p . . .
. . . . P . . .
. . . . N . . .
PPPP. PPP
R N B Q K B . R
Figure 16: Comparison of two designs–(a) without a board agent, and (b) with a board agent–in
ConversationalChess.
31
I'll move my knight from b8 to c6.
.

 | Your move is illegal.You changed the rock at a8 to knight |  | 
and move it to c6. Please check your decision and re-make your move. |  |  | 
 |  | I'llmove my knight from b8 to c6. | 

