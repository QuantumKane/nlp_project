"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    "gocodeup/codeup-setup-script",
    "gocodeup/movies-application",
    "torvalds/linux",
    'nwjs/nw.js',
    'PKUanonym/REKCARC-TSC-UHT',
    'yeasy/docker_practice',
    'leandromoreira/digital_video_introduction',
    'wulkano/Kap',
    'huihut/interview',
    'RelaxedJS/ReLaXed',
    'vercel/hyper',
    'aalansehaiyang/technology-talk',
    'danistefanovic/build-your-own-x',
    'andlabs/libui',
    'kuchin/awesome-cto',
    'AliasIO/wappalyzer',
    'yeasy/blockchain_guide',
    'shekhargulati/52-technologies-in-2016',
    'llvm/llvm-project',
    'shoelace-style/shoelace',
    'blaCCkHatHacEEkr/PENTESTING-BIBLE',
    'felixse/FluentTerminal',
    'mfornos/awesome-microservices',
    'yuanxiaosc/DeepNude-an-Image-to-Image-technology',
    'baidu-ife/ife',
    'microsoft/qlib',
    'wailsapp/wails',
    'pojala/electrino',
    'tschellenbach/Stream-Framework',
    'upgundecha/howtheysre',
    'Wei-Xia/most-frequent-technology-english-words',
    'hsoft/collapseos',
    'vendia/serverless-express',
    'corda/corda',
    'ClearURLs/Addon',
    'HIT-SCIR/ltp',
    'lynckia/licode',
    'line/armeria',
    'basho/riak',
    'mdn/browser-compat-data',
    'gothinkster/vue-realworld-example-app',
    'linuxmint/cinnamon',
    'JoseDeFreitas/awesome-youtubers',
    'jupyterhub/binderhub',
    'MacRuby/MacRuby',
    'GSA/data',
    'wandenberg/nginx-push-stream-module',
    'ionic-team/ionic-native',
    'drichard/mindmaps',
    'serverless/components',
    'ARM-software/ComputeLibrary',
    'NetDimension/NanUI',
    'ayojs/ayo',
    'MattRix/UnityDecompiled',
    'NeuronDance/DeepRL',
    'ripple/ripple-client',
    'spring-projects/greenhouse',
    'webRTC-io/webRTC.io',
    'scottslowe/learning-tools',
    'sysgears/apollo-universal-starter-kit',
    'google/skywater-pdk',
    'MobileNativeFoundation/discussions',
    'the-road-to-graphql/react-graphql-github-apollo',
    'bigtreetech/BIGTREETECH-SKR-mini-E3',
    'tsx/shireframe',
    'videojs/videojs-youtube',
    'frontend-rescue/keep-up-to-date',
    'MichalStrehovsky/zerosharp',
    'aws/jsii',
    'gdamdam/awesome-decentralized-web',
    'hahnlee/hwp.js',
    'archagon/tasty-imitation-keyboard',
    'apple/swift-format',
    'SAP/ui5-webcomponents',
    'AnyChart/GraphicsJS',
    'Teradata/kylo',
    'OpenHMD/OpenHMD',
    'alibaba/Alibaba-MIT-Speech',
    'Trinkle23897/THU-CST-Cracker',
    'ebu/awesome-broadcasting',
    'becauseofAI/HelloFace',
    'iraycd/React-Redux-Styleguide',
    'houko/SpringBootUnity',
    'mozilla/chromeless',
    'zalando/tech-radar',
    'h5bp/html5please',
    'Azure/coco-framework',
    'soruly/awesome-acg',
    'marmelo/tech-companies-in-portugal',
    'danielmahal/Rumpetroll',
    'myvin/juejin',
    'googlevr/seurat',
    'bemusic/bemuse',
    'protontypes/open-sustainable-technology',
    'lucee/Lucee',
    'lestrrat-go/jwx',
    'myvin/quietweather',
    'MicrosoftDocs/visualstudio-docs',
    'sandroasp/Microsoft-Integration-and-Azure-Stencils-Pack-for-Visio',
    'jamstack-cms/jamstack-cms',
    'google-ar/WebARonARKit',
    'jboss-developer/jboss-eap-quickstarts',
    'sakaiproject/sakai',
    'node-app/Nodelike',
    'brycejohnston/awesome-agriculture',
    'venshine/AndroidNote',
    'stellarkey/912_project',
    'dolevf/Damn-Vulnerable-GraphQL-Application',
    'AbhimanyuForiOS/GoogleNewsStandAnimation',
    'bdargan/techradar',
    'kaiwaehner/kafka-streams-machine-learning-examples',
    'alvations/pywsd',
    'Creators-of-Create/Create',
    'microsoft/TechnicalCommunityContent',
    'romanzaikin/BurpExtension-WhatsApp-Decryption-CheckPoint',
    'AntidoteDB/antidote',
    'coqui-ai/open-speech-corpora',
    'anhkgg/SuperDllHijack',
    'open-source-labs/Swell',
    'bem-site/bem-method',
    'GDGAhmedabad/Learning-Resources',
    'theseer/phpdox',
    'braziljs/weekly',
    'GoogleChromeLabs/svgomg-twa',
    'awslabs/realworld-serverless-application',
    'waylau/distributed-systems-technologies-and-cases-analysis',
    'ant-design/sunflower',
    'mercyblitz/mercyblitz.github.io',
    'apache/incubator-eventmesh',
    'tsingsee/EasyPlayer.js',
    'microsoft/Xbox-ATG-Samples',
    'automaticmode/active_workflow',
    'AdaptiveScale/lxdui',
    'Cryin/Paper',
    'jas502n/0day-security-software-vulnerability-analysis-technology',
    'upgundecha/howtheyaws',
    'unruledboy/DotNetStack',
    'att/ast',
    'raycad/devops-roadmap',
    'tyrchen/unchained',
    'OpenVisualCloud/SVT-HEVC',
    'shprink/web-components-todo',
    'MauriceConrad/Photon',
    'omarsar/nlp_highlights',
    'SaiGonSoftware/Awesome-CMS-Core',
    'mohamed-taman/Springy-Store-Microservices',
    'macosforge/dss',
    'CollaboraOnline/online',
    'yomorun/yomo',
    'hanuor/onyx',
    'Jhuster/Android',
    'rverton/webanalyze',
    'Syphon/Syphon-Framework',
    'timlrx/tailwind-nextjs-starter-blog',
    'lovasoa/dezoomify',
    'acheronfail/xi-electron',
    'RehanSaeed/EditorConfig',
    'Avnu/OpenAvnu',
    'jadianes/winerama-recommender-tutorial',
    'bevry-archive/query-engine',
    'REGoth-project/REGoth-bs',
    'rubyomr-preview/rubyomr-preview',
    'booz-allen-hamilton/The-Field-Guide-to-Data-Science',
    'dWChina/ibm-opentech-ma',
    'webRTC-io/webrtc.io-demo',
    'github/teach.github.com',
    'amiechen/codrops-scribbler',
    'ibhavikmakwana/FlutterDartTips',
    'MoZhouqi/VoiceMemos',
    'unruledboy/DatabaseStack',
    'marcrobledo/savegame-editors',
    'patrickyin/clean-architecture-android-kotlin',
    'nasa/World-Wind-Java',
    'OsamaElzero/Frontend-Tools',
    'sayanee/build-podcast',
    'nukeykt/NBlood',
    'Junnplus/blog',
    'pagedjs/pagedjs',
    'google/cauliflowervest',
    'sprylab/texturevideoview',
    'stonedreamforest/Mirage',
    'netbeast/dashboard',
    'ganeti/ganeti',
    'ushelp/EasyEE',
    'benkuper/Chataigne',
    'ganeshmani/solve_scenarios',
    'kumuluz/kumuluzee',
    'obiwanjacobi/vst.net',
    'KyleU/boilerplay',
    'wuba/WBBlades',
    'shuaishaui/springboot-technology',
    'Azure-Samples/Serverless-microservices-reference-architecture',
    'BTCPrivate/BitcoinPrivate-legacy',
    'pavansolapure/opencodez-samples',
    'aquadzn/learn-x-by-doing-y',
    'stepcode/stepcode',
    'hepsiburada/VoltranJS',
    'malikshubham827/get-me-through',
    'perifacode/comunidade',
    'sderosiaux/every-single-day-i-tldr',
    'jscherer92/Quark',
    'GoogleCloudPlatform/PerfKitExplorer',
    'MicrosoftLearning/AZ500-AzureSecurityTechnologies',
    'openMF/community-app',
    'CordovaCn/CordovaCn',
    'rdbox-intec/rdbox',
    'covarep/covarep',
    'snakajima/videoshader',
    'SAP/fundamental',
    'textileio/photos',
    'tunnckoCore/resources',
    'markzhai/DataBindingAdapter',
    'Mogztter/asciidoctor-web-pdf',
    'FederatedAI/KubeFATE',
    'apisyouwonthate/book-build-apis-2',
    'nanoant/DisableTurboBoost.kext',
    'cfpb/cfpb.github.io',
    'sdras/JS-stroll',
    'shikha-16/Women-in-Technology',
    'solettaproject/soletta',
    'Azure/kubernetes-hackfest',
    'dappledger/AnnChain',
    'redradix/posters',
    'Senscape/Dagon',
    'letsvalidate/api',
    'rinkowei/OpenGLES_Examples',
    'bigtreetech/BIGTREETECH-SKR-PRO-V1.1',
    'coremob/camera',
    'simondlr/computingcommons',
    'cypresssemiconductorco/PSoC-4-BLE',
    'eccentric-j/cljs-tui-template',
    'MapWindow/MapWindow5',
    'Zh1Cheung/Notes',
    'chrishunt/favcount',
    'dwyl/technology-stack',
    'ShielderSec/webtech',
    'KDE/yakuake',
    'oracle/oracle-db-tools',
    'sgermosen/Denunciado',
    'vkantor/MIPT_Data_Mining_In_Action_2016',
    'cqcn1991/Tech-Insight',
    'canmengfly/techmap',
    'yinxin630/blog',
    'NaomiProject/Naomi',
    'frontlinesms/frontlinesms2',
    'DevForThaiFreedom/devforthaifreedom',
    'creati8e/Finances',
    'devlinkcn/careTechnologyPartner',
    'Minecodecraft/ARDoor',
    'rcjsuen/dockerfile-language-server-nodejs',
    'shreyashankar/datasets-for-good',
    'aozhimin/MOSEC-2017',
    'florianguenther/zui53',
    'w3c/web-roadmaps',
    'grimm-co/killerbeez',
    'microsoft/BCTech',
    'lq782655835/blogs',
    'jsrn/howoldisit',
    'gtarobotics/self-driving-car',
    'DeepBCI/Deep-BCI',
    'KestrelComputer/kestrel',
    'storaged-project/udisks',
    'goupaz/goupaz.com',
    'CERN-CERT/WAD',
    'AgoraIO-Community/Solo',
    'Zhengfangxing/Book',
    'ServerlessHeroes/serverless-resources',
    'ryohey/signal',
    'atyenoria/react-native-webrtc-janus-gateway',
    'keskival/cryptocurrency-course-materials',
    'Mindwerks/XLEngine',
    'Astron/Astron',
    'miloyip/gamextech',
    'dennisjzh/GwtMobile',
    'alwintsui/scutthesis',
    'mesosphere/dcos-commons',
    'alugili/ModernArchitectureShop',
    'OpenSextant/SolrTextTagger',
    'banthagroup/fslightbox',
    'nashville-software-school/client-side-mastery',
    'fccoelho/Curso_Blockchain',
    'OpenVisualCloud/SVT-VP9',
    'signumsoftware/framework',
    'delirvfx/Delir',
    'PyDataBlog/Python-for-Data-Science',
    'kimble/dropwizard-dashboard',
    'google/apis-client-generator',
    'bigtreetech/BIGTREETECH-TFT35-V3.0',
    'MicrosoftLearning/20486-DevelopingASPNETMVCWebApplications',
    'TGmeetup/TWcommunities',
    'tcnksm/awesome-container',
    'iit-cs579/main',
    'Azure-Samples/Serverless-Eventing-Platform-for-Microservices',
    'steveonjava/JavaFX-Spring',
    'Hacking-the-Cloud/hackingthe.cloud',
    'sreich/ore-infinium',
    'ptraeg/mobile-apps-4-ways',
    'windystrife/UnrealEngine_NVIDIAGameWorks',
    'ManzDev/roadmap-web-developer-2017',
    'rule110-io/surge',
    'vslinko/ripster',
    'Unidata/siphon',
    'arduosoft/RawCMS',
    'PyCN/PTR',
    'shiffman/anti-racism-reading-list',
    'UlordChain/UlordChain',
    'HujiangTechnology/Tardis',
    'oracle/wookiee',
    'ZeeZide/5GUIs',
    'binwind8/tncode',
    'AlexxIT/WebRTC',
    'archivist/archivist',
    'huataihuang/cloud-atlas-draft',
    'anitaa1990/Today-I-Learned',
    'nuxtlabs/vue-telescope-analyzer',
    'Unidata/python-workshop',
    'wofeiwo/website-analyzer',
    'newsdev/about-int',
    'FaztTech/nodejs-mysql-links',
    'Srinivasa314/alcro',
    'bigtreetech/BTT-TFT35-E3-V3.0',
    'AdaCore/spark2014',
    'googlevr/seurat-unity-plugin',
    'adamrocker/Miracast-Sample',
    'hagata/30daysofHelloWorld',
    'kalaspuff/tomodachi',
    'oxfordinternetinstitute/InteractiveVis',
    'lvleihere/jobhere',
    'SAP/fundamental-styles',
    'zhongcaiwei/Data-visualization-technology-sharing',
    'remojansen/TechLadderIO',
    'microsoft/ts-parsec',
    'tyrchen/book_next',
    'websiddu/technology-icons',
    'hyperledger-archives/iroha-android',
    'sethm/symon',
    'GitiHubi/deepAI',
    'ashutosh1919/truvisory',
    'hust-latex/hustthesis',
    'AndrewBelt/WaveEdit',
    'jeffcrouse/CodeForArt',
    'CodedK/CUDA-by-Example-source-code-for-the-book-s-examples-',
    'groupe-sii/sonar-web-frontend-plugin',
    'andychase/gbajs2',
    'holmes89/hex-example',
    'Magin-CC/technologyPower',
    'cncf/landscapeapp',
    'diazabdulm/rumbbble',
    'projectdiscovery/wappalyzergo',
    'Yecats/dotGAME',
    'rajeshwarpatlolla/fullstack-webstuff',
    'csev/net-intro',
    'macalinao/how-to-get-an-internship',
    'anhkgg/awesome-wechat-technology',
    'microsoft/AzureSuperpowers',
    'dwyl/ISO-27001-2013-information-technology-security',
    'pmuens/discuss',
    'daltonmenezes/electron-screen-recorder',
    'kiegroup/kogito-examples',
    'opengovplatform/opengovplatform-beta',
    'intel/Intel-Pattern-Matching-Technology',
    'lvaccaro/truecrack',
    'tomoncle/Python-notes',
    'CityBaseInc/SIAC',
    'haotianteng/Chiron',
    'nixcloud/nixcloud-webservices',
    'FTD-YI/HandWriteRecognition',
    'RestComm/jain-sip',
    'Adobe-Marketing-Cloud/tools',
    'romulomourao/awesome-courses',
    'twaisu/AI-Training-and-New-Tech',
    'grab/engineering-blog',
    'anprogrammer/OpenRoads',
    'NordicSemiconductor/Android-nRF-Beacon',
    'ykameshrao/spring-mvc-angular-js-hibernate-bootstrap-java-single-page-jwt-auth-rest-api-webapp-framework',
    'leotgo/bright-souls',
    'flytxtds/AutoGBT',
    'Tillman32/CleanArchitecture',
    'jennschiffer/SimpleSlides',
    'ravisuhag/shelf',
    'neosmart/CppSQLite',
    'unicodeveloper/tech-hubs',
    'dgwozdz/HN_SO_analysis',
    'Ableton/LinkKit',
    'creativetimofficial/argon-dashboard-asp-net',
    'libyal/libfsntfs',
    'jschauma/cs631apue',
    'vipjeffreylee/ShanbayDict',
    'dduemig/Stanford-Project-Predicting-stock-prices-using-a-LSTM-Network',
    'kvartborg/hueify',
    'BillyV4/ID-entify',
    'jboss-developer/jboss-picketlink-quickstarts',
    'kelvinkamau/Vibranium',
    'WebOfTrustInfo/self-sovereign-identity',
    'covid19-dash/covid-dashboard',
    'karlphillip/GraphicsProgramming',
    'lucasmontano/learn-tech',
    'ykhwong/ppt-ndi',
    'captn3m0/the-joy-of-software-development',
    'GreenWaves-Technologies/gap_sdk',
    'vietnam-devs/crmcore',
    'bigtreetech/BIGTREETECH-SKR-E3-DIP-V1.0',
    'TorqueGameEngines/Torque2D',
    'GoogleCloudPlatform/Data-Pipeline',
    'snowshoe/snowshoe',
    'KTH/devops-course',
    'FaztTech/nodejs-imgshare',
    'nasa/OpenSPIFe',
    'erangeles/techstack',
    'timothywarner/azure-arch-crash-course',
    'hakdogan/jenkins-pipeline',
    'nokia-wroclaw/nokia-book'
]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)