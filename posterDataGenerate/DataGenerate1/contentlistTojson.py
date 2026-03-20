import os
from pathlib import Path
import json
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.JsonTools import *

# 输入content_list.json,输出content_plan.json

def get_image_size(bbox):
    x1, y1, x2, y2 = bbox
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return width, height

def transform(content_list:json) -> json:
    sections=[]
    section_index = 0
    section = {
                "id" : "",
                "title" : "",
                "content" : [],
                "tables" : [],
                "figures" : []
            }
    title=False
    metadata={}
    for index,element in enumerate(content_list):
        #遇到一个新的section标题，说明上一个section的内容已经扫完，可以加入sections
        if element["type"] == "text" and  element.get("text_level") == 1: 
            if section_index == 0 :
                section["id"] = f"section{section_index+1}"
                section["title"] = element["text"]
                section_index+=1
            else :
                sections.append(section)
                section = {
                "id" : f"section{section_index+1}",
                "title" : element["text"],
                "content" : [],
                "tables" : [],
                "figures" : []
                }
                section_index+=1
        elif element["type"] == "text":
            content=element["text"]
            section["content"].append(content)
        elif element["type"] == "image":
            figure_id = str(Path(element["img_path"]).stem)
            width,height = get_image_size(element["bbox"])
            image = {
                "fig_id" : figure_id,
                "figure_width" : width,
                "figure_height" : height,
                "figure_caption" : element.get("image_caption","")
            }
            section["figures"].append(image)
        elif element["type"] == "table":
            table_id = str(Path(element["img_path"]).stem)
            width,height = get_image_size(element["bbox"])
            table = {
                "table_id" : table_id,
                "table_width" : width,
                "table_height" : height,
                "table_caption" : element.get("table_caption","")
            }
            section["tables"].append(table)
        elif element["type"] == "list" and element.get("sub_type") == "text" :
            for text in element["list_items"]:
                section["content"].append(text)
        elif element["type"] == "header" and title == False:
            metadata={
                "title" : element["text"],
                "content" : []
            }
            title=True
        elif element["type"] == "header" and title == True:
            metadata["content"].append(element["text"])
            
    content_plan ={
        "metadata" : metadata,
        "sections": sections
    }
    #print(content_plan)
    return content_plan
if __name__=="__main__" :
    content_list=[
    {
        "type": "text",
        "text": "Reproduced: Paaβen et. al. (ICLR, 2021) ",
        "text_level": 1,
        "bbox": [
            28,
            151,
            279,
            173
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Thereproduced paper [bpa21] proposesanovel output layer for graph neural networks (GNNs),the graph edit network called (GEN).This layer yieldsa sequence of graph edits:node insertions,node deletions,node replacements,edge insertionsand edgedeletions.These finite sequences of edits,alsoreferred toasedit scriptsare general enough todescribe any graph-to-graph transformationand are not only veryinterpretablefor humans,but also computationallyefficient.These properties establish GENsasauseful tool forwork in the domainof graph timeseries prediction under the Markovianassumption. ",
        "bbox": [
            25,
            179,
            304,
            334
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/6210b10e4dec53dcffcf7a8e322ecdd877ee819c3e50e26bfb25f35f5a11132b.jpg",
        "image_caption": [],
        "image_footnote": [],
        "bbox": [
            28,
            336,
            302,
            418
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Theauthors empirically underpin their theoretical claims about GENs by showing that they perform wellina series of graph time-series prediction tests.They define several data generating processes (DGPs),from which the GEN attempts to learn the user-defined mapping functions.Ourwork reproduces these experiments and evaluates the suitability of the DGPs for the conclusions made in the original paper. ",
        "bbox": [
            25,
            424,
            304,
            527
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "DGPs & Tests ",
        "text_level": 1,
        "bbox": [
            28,
            548,
            117,
            568
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Thepaperevaluated several keyclaimsonsyntheticdatasets,generated withdata generatingrules,interpreted in the following figures. ",
        "bbox": [
            28,
            576,
            296,
            610
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/659695feac5aa0d0624e812b6b14de78250f5102b1244605f4d129fb5f6a706a.jpg",
        "image_caption": [
            "Graphcycles:Atrivial set of userdefined graph transformations without any logical rules. "
        ],
        "image_footnote": [],
        "bbox": [
            27,
            618,
            307,
            680
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/493344f248b4250b96dce1333939698abd8f0f5287eaf90812e7556b3c7046b3.jpg",
        "image_caption": [
            "Degreerules:Asetofrules fornode&edgeinsertions.(nodeswithdegree≥3aredeleted;noeswithcommonneighbor "
        ],
        "image_footnote": [],
        "bbox": [
            27,
            702,
            307,
            814
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/0ee2f2da3bed212c5c465801cd73e49d964fc45e9fb701188a439e441dcf176b.jpg",
        "image_caption": [
            "Conway'sGameofLife:Aseriesbasedonnodeedits(editingAlive/Deadbinaryfeature)onalaticegraph,adhering to Conway'sGameofLife[Gar70]. "
        ],
        "image_footnote": [],
        "bbox": [
            61,
            860,
            261,
            928
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/1aa1ccc30a6e296eaab2eab2bbedfec49807d7058e49d5dd177258281c5974b0.jpg",
        "image_caption": [
            "BooleanFormulae:RandomBoolean formulae,simplifiedwithruleslikexA-x→⊥,untiltreecannotbe simplified. "
        ],
        "image_footnote": [],
        "bbox": [
            355,
            146,
            644,
            244
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/8cb6d347d302d8d2611a0a83db88a64ca3dfd31936622e18e74830167827d6f1.jpg",
        "image_caption": [
            "PeanoAddition:Seriesoftreegraphs,modelingadditionproblemsviaPeano'sdefinitionofaddition(m+succ(n)= succ（m）+nand $m + { \\cal { O } } = m )$ using one-hot node features. "
        ],
        "image_footnote": [],
        "bbox": [
            365,
            288,
            625,
            357
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "[Re] Original experimental claims ",
        "text_level": 1,
        "bbox": [
            358,
            416,
            568,
            438
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "[bpa21] makes three experimental conclusions based on a series of experiments.√symbols below denotea successful reproduction of results. ",
        "bbox": [
            357,
            456,
            645,
            489
        ],
        "page_idx": 0
    },
    {
        "type": "list",
        "sub_type": "text",
        "list_items": [
            "GENsoutperform baselines (Variational Graph Autoencoders[KW16]& Variational Graph Recurrent nets [HHN19]) on time-series prediction tasks, generated from Graph Cycles,Degree Rules&Game of Life DGPs. ",
            "GENs achieve $100 \\%$ accuracy on time-series prediction tasks on graphs, generatedfrom Boolean Formulae&Peano Addition DGPs. ",
            "？Theruntime of forward passes of a GEN scales sub-quadratically as the number of nodes ina graph increases.The runtime of training back-passes scalesapproximatelylinearly. "
        ],
        "bbox": [
            358,
            491,
            643,
            630
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/5e24f2829b36b74e18ea4569c7bd5c57d2e0428e0bc4adcd80389600c9db0ae6.jpg",
        "image_caption": [
            "Theruntime of graph scale dependence.Results forthe backwardpasses are not consistent with the claim. "
        ],
        "image_footnote": [],
        "bbox": [
            358,
            639,
            641,
            781
        ],
        "page_idx": 0
    },
    {
        "type": "table",
        "img_path": "images/ae4a6a1de686a68b5f01a7c077b996f70fef6180a7af0b80dde7094d7f7af9aa.jpg",
        "table_caption": [],
        "table_footnote": [],
        "table_body": "<table><tr><td>Pass direction</td><td>Edge filtering</td><td>Log-log linear slope fit</td></tr><tr><td rowspan=\"2\">Forward</td><td>Flexible</td><td>1.38 ± 0.02</td></tr><tr><td>Constant</td><td>1.31 ± 0.02</td></tr><tr><td rowspan=\"2\">Backward</td><td>Flexible</td><td>1.30 ± 0.01</td></tr><tr><td>Constant</td><td>1.69 ± 0.10</td></tr></table>",
        "bbox": [
            367,
            827,
            497,
            935
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Theruntime scaling evaluation was carried out on the ArXivcitationnetwork[LKF05]withthegraphvariants generatedbyadifferentnumber ofmonthsconsidered. ",
        "bbox": [
            369,
            947,
            493,
            975
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/71513a552e56ac9e264d1d467c2769e7472fced19f8dd646df8f663e7697af13.jpg",
        "image_caption": [],
        "image_footnote": [],
        "bbox": [
            500,
            832,
            635,
            941
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "While the focus here is speed,we have to note that the experiment intheoriginalpaperfailstooptimize the criterion loss,thus castingdoubt on theresults. ",
        "bbox": [
            510,
            947,
            635,
            976
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Improving the experimental setup ",
        "text_level": 1,
        "bbox": [
            695,
            151,
            909,
            175
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Thefacts that graph-to-graph transitionsare deterministic and that the space of unique graphs that may be generated by the DGPs is limited (as shown in the table below),arose some concern about the experimental setup:Does the solver generalize,or does it simply memorize the graphto-graph transitions? ",
        "bbox": [
            694,
            185,
            968,
            271
        ],
        "page_idx": 0
    },
    {
        "type": "table",
        "img_path": "images/04a1056d25bafc0cb02cb0bc2eb891f84c4f97fa64f07394d9ba9956cd1d596a.jpg",
        "table_caption": [],
        "table_footnote": [],
        "table_body": "<table><tr><td></td><td>Graph cycles</td><td>Degree rules</td><td>Game of life</td><td>Boolean formulae</td><td>Peano addition</td></tr><tr><td># unique graphs</td><td>9</td><td>12346</td><td>2100</td><td>10788</td><td>34353</td></tr></table>",
        "bbox": [
            695,
            275,
            969,
            337
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "We reproduced the claims (1)and (2) with the following adjustments: ",
        "bbox": [
            695,
            345,
            944,
            361
        ],
        "page_idx": 0
    },
    {
        "type": "list",
        "sub_type": "text",
        "list_items": [
            "Increased cardinality of test time series $( 5 \\to 1 0 0 )$ ",
            "Ensured no duplicates between train& test set ",
            "·Used established random graph generation methods (ie.Erdäs-Renyi) "
        ],
        "bbox": [
            696,
            364,
            962,
            414
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Wenoticed that most sampled graphsin the tree dynamic graph experimentswereun-simplifyable,soconstraintswererelaxed here. ",
        "bbox": [
            695,
            421,
            966,
            455
        ],
        "page_idx": 0
    },
    {
        "type": "image",
        "img_path": "images/b1ccf1c5a97bb77ee3922d8af0309938f2837d29b137b8e378ce7308cc24e932.jpg",
        "image_caption": [
            "Results were generally worse,but still within a reasonable margin of error. "
        ],
        "image_footnote": [],
        "bbox": [
            695,
            496,
            966,
            640
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Concluding reproduction notes ",
        "text_level": 1,
        "bbox": [
            695,
            664,
            894,
            686
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "Our experimental results conclusively show that most of the claims in the original work hold.However，our work beyond the original paper emphasizes theneed to payattention to the experimental setup,especially whenworking with synthetically generated data，sampled from functions, rather than gathered froman external system. ",
        "bbox": [
            693,
            697,
            966,
            783
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "References ",
        "text_level": 1,
        "bbox": [
            695,
            806,
            747,
            820
        ],
        "page_idx": 0
    },
    {
        "type": "list",
        "sub_type": "text",
        "list_items": [
            "[bpa21] PaaBen,Benjamin,etal.\"Graphedit networks.\"In: International Conference ",
            "[Gar70] Martin Gardner.“The fantastic combinations of John Conway's newsolitaire gameoflife.In:Sc.Am.,223:20-123,1970 ",
            "[KW16] ThomasN.Kipfand MaxWeling.“Variational graphauto-encoders\"In: Proceedings of the NIPS2016Workshop onBayesian Deep Learning，2016 "
        ],
        "bbox": [
            696,
            822,
            899,
            894
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "[HHN19] Hajiramezanali,Ehsan,et.al.“Variational graph recurrent neural networks.” ",
        "bbox": [
            695,
            898,
            901,
            933
        ],
        "page_idx": 0
    },
    {
        "type": "text",
        "text": "[LKF05]Leskovec,Jure,Jon Kleinberg,and Christos Faloutsos.\"Graphs over time: densification laws，shrinkingdiametersandpossibleexplanations.\"ln:Proceedingsof theeleventh ACM SIGKDD international conference on Knowledge discovery indata ",
        "bbox": [
            695,
            937,
            902,
            984
        ],
        "page_idx": 0
    },
    {
        "type": "header",
        "text": "[Re] Graph Edit Networks ",
        "bbox": [
            27,
            56,
            272,
            92
        ],
        "page_idx": 0
    },
    {
        "type": "header",
        "text": "ta Science @UL-FRI ",
        "bbox": [
            525,
            44,
            647,
            109
        ],
        "page_idx": 0
    },
    {
        "type": "header",
        "text": "University ofLjubljana Faculty of Computer and ",
        "bbox": [
            724,
            65,
            823,
            109
        ],
        "page_idx": 0
    },
    {
        "type": "header",
        "text": "NEURALINFORMATION PROCESSINGSYSTEMS ",
        "bbox": [
            833,
            27,
            976,
            121
        ],
        "page_idx": 0
    },
    {
        "type": "header",
        "text": "Vid Stropnik,Marusa Orazem ",
        "bbox": [
            27,
            108,
            137,
            124
        ],
        "page_idx": 0
    },
    {
        "type": "footer",
        "text": "1 ",
        "bbox": [
            926,
            899,
            989,
            992
        ],
        "page_idx": 0
    }
]
    json_data=transform(content_list)
    with open('./planjson.json','w',encoding='utf-8') as f:
        json.dump(json_data,f,ensure_ascii=False,indent=2)