5 LimitationsandDiscussion
Inthispaper,wepresentanorthogonalapproachtoimprovetheperformanceoflanguagemodels
using multi-agent debate. We find that the approach is simple and effective across a wide set of
differentreasoningandvaliditylanguagemodelingtasks.
Limitations. Incomparisontootherpromptingtechniques, ourmultiagentdebateprocedureis
morecomputationallyexpensive,asitrequiresbothmultiplelanguagegenerations,andanunderlying
debate procedure. However, we believe that this approach may be seen as a method to generate
additionaldatathatmaybedistilledbacktoself-improvetheoriginalbasemodel.
Further,weobservedthatasdebatesbecamelongerinduration,currentlanguagemodelssometimes
struggled to fully process the entire debate input, and typically only focused on the most recent
generations. Webelievethatthisperformancewillbealleviatedwithlonger-contextandimproved
languagemodelsorbysummarizingearlyportionsofthedebate.
Finally,wefoundthatwhiledebatestypicallyconvergedintosinglefinalanswers,theseanswerswere
notnecessarilycorrect. Despiteanswersbeingincorrect,languagemodelswouldconfidentlyaffirm
thattheiransweriscorrectandconsistentwithallotheragentresponses. Webelievethisresultisin
partduetothefactthatLMsdonotcorrectlyexpresstheiruncertaintywhengeneratingresponses,
andbelievethatotherorthogonalapproachestoimprovethisperformancewouldimprovetheresults
ofmultiagentdebate.
References
[1] J.-B.Alayrac,J.Donahue,P.Luc,A.Miech,I.Barr,Y.Hasson,K.Lenc,A.Mensch,K.Millican,
M.Reynolds,etal. Flamingo: Avisuallanguagemodelforfew-shotlearning. NeurIPS,2022.
URLhttps://arxiv.org/abs/2204.14198. 9
[2] P.F.Christiano,J.Leike,T.Brown,M.Martic,S.Legg,andD.Amodei. Deepreinforcement
learningfromhumanpreferences. InNeuralInformationProcessingSystems,2017. 9
[3] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek,
J.Hilton, R.Nakano, etal. Trainingverifierstosolvemathwordproblems. arXivpreprint
arXiv:2110.14168,2021. 5,9
[4] Y.Du,S.Li,andI.Mordatch. Compositionalvisualgenerationwithenergybasedmodels. In
AdvancesinNeuralInformationProcessingSystems,2020. 9
[5] Y. Du, C. Durkan, R. Strudel, J. B. Tenenbaum, S. Dieleman, R. Fergus, J. Sohl-Dickstein,
A.Doucet,andW.Grathwohl. Reduce,reuse,recycle: Compositionalgenerationwithenergy-
baseddiffusionmodelsandmcmc. arXivpreprintarXiv:2302.11552,2023. 9
[6] Fsmosca. Fsmosca/pgn-standard: Portablegamenotationspecificationandimplementation
guide. URLhttps://github.com/fsmosca/PGN-Standard. 5
[7] K.Guu,K.Lee,Z.Tung,P.Pasupat,andM.-W.Chang.REALM:Retrieval-augmentedlanguage
modelpre-training. arXivpreprintarXiv:2002.08909,2020. 9
[8] D.Hendrycks,C.Burns,S.Basart,A.Zou,M.Mazeika,D.Song,andJ.Steinhardt. Measuring
massivemultitasklanguageunderstanding. arXivpreprintarXiv:2009.03300,2020. 7
[9] G.Irving,P.Christiano,andD.Amodei. Aisafetyviadebate. arXivpreprintarXiv:1805.00899,
2018. 9
[10] S.Kadavath,T.Conerly,A.Askell,T.Henighan,D.Drain,E.Perez,N.Schiefer,Z.H.Dodds,
N.DasSarma,E.Tran-Johnson,etal. Languagemodels(mostly)knowwhattheyknow. arXiv
preprintarXiv:2207.05221,2022. 7,9
[11] T.Kojima,S.S.Gu,M.Reid,Y.Matsuo,andY.Iwasawa. Largelanguagemodelsarezero-shot
reasoners. arXivpreprintarXiv:2205.11916,2022. 2,6,9
10
