var NAN_REPR="---";var MAX_TILE_HEADER_LEN=30;var MAX_TILE_HEADER_LEN_PIX=320;var SENSOR_DISCONNECTED=999;var SENSOR_DISCONNECTED2=65535;var rebuildEditableParameters=false;var tilesETFlag=false;var disableTileMode=false;var tilesResChange=false;var PARAMETERS_CONN={"tempCO":["CO_TEMP_SET","CO_TEMP_SET"],"tempCWU":["CWU_SET_TEMP","CWU_SET_TEMP"],"mixerTemp1":["MIX_SET_TEMP_1","SET_TEMP_H_1"],"mixerTemp2":["MIX_SET_TEMP_2","SET_TEMP_H_2"],"mixerTemp3":["MIX_SET_TEMP_3","SET_TEMP_H_3"],"mixerTemp4":["MIX_SET_TEMP_4","SET_TEMP_H_4"],"mixerTemp5":["MIX_SET_TEMP_5","SET_TEMP_H_5"],"mixerTemp6":["MIX_SET_TEMP_6","SET_TEMP_H_6"],"mixerTemp7":["MIX_SET_TEMP_7","SET_TEMP_H_7"],"mixerTemp8":["MIX_SET_TEMP_8","SET_TEMP_H_8"],"T2":["TzCWU"],"ecoSterTemp1":["STER_TEMP_DAY_1","STER_TEMP_NIGHT_1","STER_TEMP_SET_PARTY_1","STER_TEMP_SET_SUMMER_1","STER_TEMP_ANTIFREEZ_1","STER_MODE_1","WORK_MODE_H_1"],"ecoSterTemp2":["STER_TEMP_DAY_2","STER_TEMP_NIGHT_2","STER_TEMP_SET_PARTY_2","STER_TEMP_SET_SUMMER_2","STER_TEMP_ANTIFREEZ_2","STER_MODE_2","WORK_MODE_H_2"],"ecoSterTemp3":["STER_TEMP_DAY_3","STER_TEMP_NIGHT_3","STER_TEMP_SET_PARTY_3","STER_TEMP_SET_SUMMER_3","STER_TEMP_ANTIFREEZ_3","STER_MODE_3","WORK_MODE_H_3"],"ecoSterTemp4":["STER_TEMP_DAY_4","STER_TEMP_NIGHT_4","STER_TEMP_SET_PARTY_4","STER_TEMP_SET_SUMMER_4","STER_TEMP_ANTIFREEZ_4","STER_MODE_4","WORK_MODE_H_4"],"ecoSterTemp5":["STER_TEMP_DAY_5","STER_TEMP_NIGHT_5","STER_TEMP_SET_PARTY_5","STER_TEMP_SET_SUMMER_5","STER_TEMP_ANTIFREEZ_5","STER_MODE_5","WORK_MODE_H_5"],"ecoSterTemp6":["STER_TEMP_DAY_6","STER_TEMP_NIGHT_6","STER_TEMP_SET_PARTY_6","STER_TEMP_SET_SUMMER_6","STER_TEMP_ANTIFREEZ_6","STER_MODE_6","WORK_MODE_H_6"],"ecoSterTemp7":["STER_TEMP_DAY_7","STER_TEMP_NIGHT_7","STER_TEMP_SET_PARTY_7","STER_TEMP_SET_SUMMER_7","STER_TEMP_ANTIFREEZ_7","STER_MODE_7","WORK_MODE_H_7"],"ecoSterTemp8":["STER_TEMP_DAY_8","STER_TEMP_NIGHT_8","STER_TEMP_SET_PARTY_8","STER_TEMP_SET_SUMMER_8","STER_TEMP_ANTIFREEZ_8","STER_MODE_8","WORK_MODE_H_8"]};var PARAMETERS_CONN_DYNAMIC_CONN={}
var RM_PARAMETERS_CONN={"tempCO":"1280","tempCWU":"1281","mixerTemp1":"1287","mixerTemp2":"1288","mixerTemp3":"1289","mixerTemp4":"1290","mixerTemp5":"1291","mixerTemp6":"1292"};var RM_PARAMETERS_850I_CONN={"CWU_WORK_MODE":"2057","WORK_MODE_H_1":"2050","WORK_MODE_H_2":"2051","WORK_MODE_H_3":"2052","WORK_MODE_H_4":"2053","WORK_MODE_H_5":"2054","WORK_MODE_H_6":"2055","WORK_MODE_H_7":"2056"};var WEATHER_CONTROL_850I={"mixerTemp1":"REGULATION_H_1","mixerTemp2":"REGULATION_H_2","mixerTemp3":"REGULATION_H_3","mixerTemp4":"REGULATION_H_4","mixerTemp5":"REGULATION_H_5","mixerTemp6":"REGULATION_H_6","mixerTemp7":"REGULATION_H_7",};var STER_MODE_PARAM=['STER_MODE_','WORK_MODE_H_']
var STER_TEMP_PARAMS_MAP=[['harm','STER_TEMP_NIGHT_','STER_TEMP_DAY_','STER_TEMP_NIGHT_','','STER_TEMP_SET_PARTY_','STER_TEMP_SET_SUMMER_','STER_TEMP_ANTIFREEZ_','STER_TEMP_DAY_'],['harm','harmdn','DAY_TEMP_H_','NIGHT_TEMP_H_',''],];var THERM_MODE_EDIT_TILES=['tempCWU']
var OTHER_MODE_EDITS=['CWU_WORK_MODE']
var TILES_ICON_MAP={"ecoSterTemp1":[0,-1],"ecoSterTemp2":[0,-1],"ecoSterTemp3":[0,-1],"ecoSterTemp4":[0,-1],"ecoSterTemp5":[0,-1],"ecoSterTemp6":[0,-1],"ecoSterTemp7":[0,-1],"ecoSterTemp8":[0,-1],"fanPower":[0,0],"tempCWU":[0,-2]
};var STER_MODES_IMGS_ICONS=[[[-2,-2],[-4,0],[-5,-1],[-4,-1],[-3,-1],[-5,-2],[-4,-2],[-3,-4],[-1,-1]],[[-3,0],[-4,-3],[-2,-3],[-2,-4],[-5,0]]]
var TILES_ICON_MULTIPLIERH=6;var TILES_ICON_MULTIPLIERW=6;var TILES_ICON_WHPROP=1.29;var TILES_ICON_WHPROPOFF=1.33;var TILES_MODE_ICON_WPROC=0.65;var TILES_TYPE_ICON_WPROC=0.5;var SCREEN_CANVAS_SIZES=[{"canvasw":248,"canvash":216,"canvasheaderh":53,"canvaswmarg":10,"canvaswpadd":10},{"canvasw":165,"canvash":144,"canvasheaderh":43,"canvaswmarg":7,"canvaswpadd":7},{"canvasw":135,"canvash":118,"canvasheaderh":33,"canvaswmarg":5,"canvaswpadd":5},]
var DEL_TILE_IMG="remove_tileico.jpg";var MAX_FRAME_SEED=30;var MAX_ANIMATION_VALUE=100;var tiles_type_temp="tile_temp";var tiles_type_temp_ro="tile_temp_ro";var tiles_type_temp_wave="tile_temp_wave";var tiles_type_level="tile_level";var tiles_type_flame="tile_flame";var tiles_type_fan="tile_fan";var tiles_type_pump="tile_pump";var tiles_type_stream="tile_stream";var tiles_type_power="tile_power";var tiles_type_text="tile_text";var tiles_type_text_icon="tile_text_icon";var tiles_type_heater="tile_heater"
var tiles_type_compressor="tile_compressor"
var tiles_type_b2="tile_b2"
var tiles_type_b3b4="tile_b3b4"
var tiles_temp=[];var tiles_temp_ro=[];var tiles_temp_wave=[];var tiles_level=[];var tiles_flame_states=[];var tiles_fan_states=[];var tiles_pump_states=[];var tiles_feeder_states=[];var tiles_stream=[];var tiles_power=[];var tiles_text=[];var tiles_text_icon=[];var tiles_heater_states=[];var tiles_compressor_states=[];var tiles_b2=[];var tiles_b3b4=[];var tiles_canvas_sizeclass=0;var tiles_canvas_width=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvasw;var tiles_canvas_height=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvash;var tiles_canvas_totalmarg=(2*SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvaswmarg)+(2*SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvaswpadd);var tiles_canvas_headerh=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvasheaderh;var tiles_canvas_innerw=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvasw-(2*SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvaswpadd);var tiles_canvas_iconw=tiles_canvas_innerw*0.3;var tiles_canvas_valuew=tiles_canvas_innerw-tiles_canvas_iconw;var tiles_stop_animation=true;var tiles_animation_run=false;var tiles_currentDataUpdate=0;var tiles_tab=[];var tiles_dict={};var deletedTiles=[];var tiles_params=[]
var new_tiles_params=[]
var regParams=Object();function Param(val,str,unit,num){if(val!=undefined)
this.val=val;else
this.val=null;if(str!=undefined)
this.str=str;else
this.str=NAN_REPR;if(unit!=undefined)
this.unit=unit;else
this.unit=null;if(num!=undefined)
this.num=num;if(unit!=undefined&&str!=NAN_REPR)
this.strWithUnit=this.str+unit;else if(str!=NAN_REPR)
this.strWithUnit=this.str+((unit!=undefined)?unit:'');else
this.strWithUnit=NAN_REPR;if((unit!=undefined)&&(typeof val=="number")&&(val<100)&&(val%1!==0)){this.str=this.val.toFixed(1)
this.strWithUnitFloat=this.val.toFixed(1)+unit;}else if(str!=NAN_REPR){this.strWithUnitFloat=this.str+((unit!=undefined)?unit:'');}else{this.strWithUnitFloat=NAN_REPR;}
this.getParamUnit=function(){return(this.unit!=undefined&&this.unit!=null)?this.unit:'';};}
var regParamsPrecision={"boilerPowerKW":1,"boilerPower":0,"fuelStream":1,"ecoSterTemp":1,"ecoSterSetTemp":1,"tempExternalSensor":1,"lambdaSet":1,"lambdaLevel":1,"thermoTemp":1,"thermoSetTemp":0};var regParamsUnit={'T1':'°C','T2':'°C','T3':'°C','T4':'°C','T5':'°C','T6':'°C','P1':'%','P2':'%','H':'','TzCWU':'°C','tempCO':'°C','tempCOSet':'°C','tempCWU':'°C','tempCWUSet':'°C','tempOpticalSensor':'%','fanPower':'%','fuelLevel':'%','tempUpperBuffer':'°C','tempLowerBuffer':'°C','tempUpperSolar':'°C','tempLowerSolar':'°C','tempFireplace':'°C','tempExternalSensor':'°C','tempBack':'°C','fuelStream':'kg/h','tempFeeder':'°C','tempFlueGas':'°C','boilerPowerKW':'kW','boilerPower':'%','ecoSterTemp1':'°C','ecoSterTemp2':'°C','ecoSterTemp3':'°C','ecoSterTemp4':'°C','ecoSterTemp5':'°C','ecoSterTemp6':'°C','ecoSterTemp7':'°C','ecoSterTemp8':'°C','ecoSterSetTemp1':'°C','ecoSterSetTemp2':'°C','ecoSterSetTemp3':'°C','ecoSterSetTemp4':'°C','ecoSterSetTemp5':'°C','ecoSterSetTemp6':'°C','ecoSterSetTemp7':'°C','ecoSterSetTemp8':'°C','mixerTemp1':'°C','mixerTemp2':'°C','mixerTemp3':'°C','mixerTemp4':'°C','mixerTemp5':'°C','mixerTemp6':'°C','mixerTemp7':'°C','mixerTemp8':'°C','mixerSetTemp1':'°C','mixerSetTemp2':'°C','mixerSetTemp3':'°C','mixerSetTemp4':'°C','mixerSetTemp5':'°C','mixerSetTemp6':'°C','mixerSetTemp7':'°C','mixerSetTemp8':'°C','lambdaLevel':'%','lambdaSet':'%','LPTc':'°C','LPTsc':'°C','BHThc':'°C','LPTbackc':'°C','LPTbc':'°C','totalGain':'kWh','blowFan1BlowPower':'%','blowFan2BlowPower':'%','tempExchanger':'°C','tempAirIn':'°C','tempAirOut':'°C','thermoTemp':'°C','thermoSetTemp':'°C','fanPowerExhaust':'%'};var NO_TEMP_SET_STATUS_CODE=128;var set_temperatures_status_dict={"tempCWUSet":"statusCWU","tempCOSet":"statusCO","CWU_SET_TEMP":"statusCWU","CO_TEMP_SET":"statusCO"};function shouldShowParam(paramName){if(paramName in set_temperatures_status_dict){const p_status=regParams[set_temperatures_status_dict[paramName]];return!((p_status!==undefined)&&(p_status.val===NO_TEMP_SET_STATUS_CODE));}
return true;}
function getRegParamIfExists(name,bit,description){if(name!=undefined&&name!=null){if(name.indexOf('_b2')!=-1){name=name.substring(0,(name.length-3))}
if(name.indexOf('_b3b4')!=-1){name=name.substring(0,(name.length-5))}}
if((regParams[name]===undefined)||!shouldShowParam(name)){return new Param();}else{if(bit==null){return regParams[name];}
else{const val=getValueBit(regParams[name].val,bit);let stringVal="";if(description!=undefined){stringVal=(val?translate(description+" on"):translate(description+" off"));}
else{stringVal=(val?translate("on"):translate("off"));}
return new Param(val,stringVal,null);}}}
var Mode={0:"modeTurnOff",1:"modeStop",2:"modeKindle",3:"modeWork",4:"modeSupervision",5:"modeHalt",6:"modeCleaning",7:"modeExtinction",8:"modeAlarm",9:"modeManual",10:"modeUnsealing",11:"modeOther",12:"modeStabilization",13:"modePurge",14:"modeCheckFlame",15:"modeFlameLosing",16:"modePrevention",17:"modeWorkGrate",18:"modeSupervisionGrate",19:"modeCalibration",20:"modeMaintain",21:"modeAfterburning",22:"modeChimneySwep",23:"modeHeats",24:"modeOpenDoor",25:"modeCooling",26:"modeSafe"};function getModeParamIfExists(){const modeType=getRegParamIfExists("mode").str;let modeName=(modeType==NAN_REPR?modeType:translate(Mode[modeType]));if((modeName===null)||(modeName===undefined)){modeName="---";}
return modeName;}
function createCurrentParamsDict(params,units,numbers){regParams={}
for(p in params){var value=params[p];if(isDeviceGm3Conf()){var unit=null;var num=null;if(units!=undefined){unit=units[p]}
if(numbers!=undefined){num=numbers[p]}
regParams[p]=new Param(value,convertValToStr(value),PARAMETER_UNIT[unit],num);}
else{if(p=="lambdaSet"||p=="lambdaLevel"){value/=10;}else if(p=="boilerPowerKW"){if(params[p]>99)
regParamsPrecision["boilerPowerKW"]=0;else
regParamsPrecision["boilerPowerKW"]=1;}
var precision=0;if(p in regParamsPrecision){precision=regParamsPrecision[p];}else if(p.slice(0,-1)in regParamsPrecision){precision=regParamsPrecision[p.slice(0,-1)];}
regParams[p]=new Param(value,convertValToStr(value,precision),regParamsUnit[p]);}}}
function setRegTime(second,minute,hour,day,dayOfWeek,month,year){$("#second").text(formatToTwoChar(second));$("#minute").text(formatToTwoChar(minute));$("#hour").text(formatToTwoChar(hour));$("#day").text(formatToTwoChar(day));$("#dayOfWeek").text(translate(ENUM_TYPE[200][dayOfWeek]));$("#month").text(formatToTwoChar(month));$("#year").text(year);}
function formatToTwoChar(val){if(val!=undefined)
return(val.toString()).length==2?val:"0"+val;else
return NAN_REPR;}
function setParamAndUpdate(params,units,numbers,schemaparams,tilesparams){if(tilesparams!=undefined&&tilesparams!=null){regConfig=true;}
createCurrentParamsDict(params,units,numbers);if(!$.isEmptyObject(schemaparams)){SchemaParamsWithSettings=schemaparams;}
if(!$.isEmptyObject(tilesparams)){new_tiles_params=tilesparams
createTilesET();}else{updateStatic();}
tiles_currentDataUpdate+=1;if(updater.controller_.protocol_type=="gm3_pomp"){setRegTime(params["RTCsecond"],params["RTCminute"],params["RTChour"],params["RTCday"],params["RTCweekday"],params["RTCmonth"],params["RTCyear"]);}}
function State(tile,frameWidth,frameHeight,frames,label,valueint){this.tile=tile;this.frameWidth=frameWidth;this.frameHeight=frameHeight;this.frames=frames;this.frameNo=0;this.timeDiff=0;this.label=label;this.valueint=valueint;}
function convertValToStr(val,precision,max_value){if(typeof val=='boolean'){return Boolean(val).toString();}else if(typeof val=='string'){return val;}
if(val!=null&&val!=SENSOR_DISCONNECTED&&val!=SENSOR_DISCONNECTED2&&!isNaN(val)){if(!isDeviceGm3Conf()){if(!precision){precision=0;return val.toFixed(0);}
val=parseFloat(val);if(max_value){val=Math.min(val,max_value);}
val=val.toFixed(precision+3);val=val.substring(0,val.length-3);}
return val;}
return NAN_REPR;}
function setDPI(canvas,dpi){if(!canvas.style.width)
canvas.style.width=canvas.width+'px';if(!canvas.style.height)
canvas.style.height=canvas.height+'px';const scaleFactor=dpi/96;canvas.width=Math.ceil(canvas.width*scaleFactor);canvas.height=Math.ceil(canvas.height*scaleFactor);const ctx=canvas.getContext('2d');ctx.scale(scaleFactor,scaleFactor);}
function changeResolution(canvas,scaleFactor){if(!canvas.style.width)
canvas.style.width=canvas.width+'px';if(!canvas.style.height)
canvas.style.height=canvas.height+'px';canvas.width=Math.ceil(canvas.width*scaleFactor);canvas.height=Math.ceil(canvas.height*scaleFactor);const ctx=canvas.getContext('2d');ctx.scale(scaleFactor,scaleFactor);}
function setCanvasResParams(){$('#tilesMain').find('canvas').each(function(){changeResolution($(this)[0],Math.round(window.devicePixelRatio))});}
function checkTilesSizeByRes(screenw){var tmp_sizeclass=0;if(screenw<700){tmp_sizeclass=2}else if(screenw<1300){tmp_sizeclass=1}
if(tiles_canvas_sizeclass!=tmp_sizeclass){tiles_canvas_sizeclass=tmp_sizeclass;tiles_canvas_width=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvasw;tiles_canvas_height=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvash;tiles_canvas_totalmarg=(2*SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvaswmarg)+(2*SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvaswpadd);tiles_canvas_headerh=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvasheaderh;tiles_canvas_innerw=SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvasw-(2*SCREEN_CANVAS_SIZES[tiles_canvas_sizeclass].canvaswpadd);tiles_canvas_iconw=tiles_canvas_innerw*0.3;tiles_canvas_valuew=tiles_canvas_innerw-tiles_canvas_iconw;return true;}
return false}
function centerTiles(){var reloadTiles=checkTilesSizeByRes($(window).width());var tilesPanelWidth=$('#secData').width();var totalTileWidth=tiles_canvas_width+tiles_canvas_totalmarg;var tilesNumber=Math.floor(tilesPanelWidth/totalTileWidth);var tilesWidth=tilesNumber*totalTileWidth;if(tilesWidth>tilesPanelWidth){console.log("Warning: centerTiles(): tilesWidth ("+tilesWidth+") is higher than window width!");tilesWidth=tilesPanelWidth;}
$('#tilesMain').css("width",tilesWidth+"px");return reloadTiles;}
function addTile(tile,type){if(type==tiles_type_temp){tiles_temp.push(tile);}else if(type==tiles_type_temp_ro){tiles_temp_ro.push(tile);}else if(type==tiles_type_temp_wave){tiles_temp_wave.push(tile);}else if(type==tiles_type_level){tiles_level.push(tile);}else if(type==tiles_type_flame){tiles_flame_states.push(new State(tile,93,69,5,"flameLabel",true));}else if(type==tiles_type_fan){tiles_fan_states.push(new State(tile,97,69,8,"ventPowerLabel",true));}else if(type==tiles_type_pump){tiles_pump_states.push(new State(tile,71,66,4));}else if(type==tiles_type_stream){tiles_feeder_states.push(new State(tile,74,33,10,"feederLabel",false));}else if(type==tiles_type_power){tiles_power.push(tile);}else if(type==tiles_type_text){tiles_text.push(tile);}else if(type==tiles_type_text_icon){tiles_text_icon.push(tile);}else if(type==tiles_type_heater){tiles_heater_states.push(new State(tile,90,67,9));}else if(type==tiles_type_compressor){tiles_compressor_states.push(new State(tile,93,70,12));}else if(type==tiles_type_b2){tiles_b2.push(tile);}else if(type==tiles_type_b3b4){tiles_b3b4.push(tile);}else{console.log("Warning: addTile(): unknown tile type!");}}
function getTileString(name,footer,clickable,popupMethod,closable,closed,disabled,addparam)
{if(disabled==undefined){disabled=false;if(name in PARAMETERS_CONN){for(var i=0;i<PARAMETERS_CONN[name].length;i+=1){if(PARAMETERS_CONN[name][i]in changedParams){disabled=true;}}}}
var disabledPart=(disabled?' tiledisabled':'');var closedPart=(closed?' hidden':'');var clickPart=((clickable)?'onclick="'+popupMethod+'"':'');if(clickable&&!disabled){clickPart=' class="tilebutton" '+clickPart;}
closable=true;var tileStr='<article class="display'+closedPart+disabledPart+'">'
+'<canvas'+clickPart+' id="tilesCanvas_'+name+'" width="'+tiles_canvas_width+'px" height="'+tiles_canvas_height+'px"></canvas>'
+'<footer><div id="tilesFooter_'+footer+'"><div class="titleHeaderTitlePanel" style="height: '+tiles_canvas_headerh+'px; width: '+tiles_canvas_width+'px">'+getTileHeaderTitle(name,addparam)+'</div>'+getTileClosablePart(closable,name)+'</div></footer>'
+'</article>'
return tileStr;}
function getTileHeaderIcon(name){if(name in TILES_ICON_MAP){var whint=parseInt(TILES_TYPE_ICON_WPROC*tiles_canvas_headerh);return'<i class="tileIconCommon" style="height: '+whint+'px; width: '+whint+'px; background-size: '+TILES_ICON_WHPROP*TILES_ICON_MULTIPLIERW*whint+'px '+TILES_ICON_MULTIPLIERH*whint+'px; background-position: '+TILES_ICON_MAP[name][0]*whint*TILES_ICON_WHPROPOFF+'px '+TILES_ICON_MAP[name][1]*whint+'px;"></i>';}else{return'';}}
function getTileHeaderTitle(name,addparam){if(addparam){return'<div class="tileHeaderLeft" style="width: '+0.89*tiles_canvas_width+'px;">'+getTileHeaderIcon(name)+'<label></label></div><div class="tileHeaderRight" style="width: '+0.11*tiles_canvas_width+'px;"></div></div>'}else{return'<div class="tileHeaderLeft">'+getTileHeaderIcon(name)+'<label></label></div></div>'}}
function getTileClosablePart(closable,name){return''}
function cleanTiles(){tiles_temp=[];tiles_temp_ro=[];tiles_temp_wave=[];tiles_level=[];tiles_flame_states=[];tiles_fan_states=[];tiles_pump_states=[];tiles_feeder_states=[];tiles_stream=[];tiles_power=[];tiles_text=[];tiles_text_icon=[];tiles_heater_states=[];tiles_compressor_states=[];tiles_b2=[];tiles_b3b4=[];$('#tilesMain').empty();}
function createTiles(tab){if(isDeviceGm3()){if(tilesETFlag&&!$.isEmptyObject(tiles_params)){createTilesET();}else{createTilesGm(tab);}}
else{createTilesEm(tab);}
translateTilesHeaders();tilesResChange=false;}
function updateStatic(){if(isDeviceGm3()){updateStaticGm();}
else{updateStaticEm();}
schemaUpdateValues();}
function contentAnimate(timeLast){if(tiles_stop_animation||ngp_hide("home")){tiles_animation_run=false;return;}
tiles_animation_run=true;var date=new Date();var timeDiff=(date.getTime()-timeLast)/1000;for(var i in tiles_flame_states){var param=getRegParamIfExists(tiles_flame_states[i].tile.memberName_);if(param.val>50)
animate(tiles_flame_states[i],timeDiff/3,document.getElementById("flame_image_large"));else
animate(tiles_flame_states[i],timeDiff/3,document.getElementById("flame_image_small"));}
animateTilesTab(tiles_fan_states,timeDiff*3,"fan_image");animateTilesTab(tiles_pump_states,timeDiff,"pump_image");animateTilesTab(tiles_feeder_states,timeDiff,"feeder_image");animateTilesTab(tiles_heater_states,timeDiff*10,"heater_image","heater");animateTilesTab(tiles_compressor_states,timeDiff*10,"compressor_image","compressor");requestAnimFrame(function(){contentAnimate(date.getTime());});}
function animateTilesTab(tab_state,timeDiff,imageFile,description){for(var i in tab_state){animate(tab_state[i],timeDiff,document.getElementById(imageFile),description);}}
function getFrameSizeDensityFactor(img){if(img!=undefined&&img!=null){if(typeof img.currentSrc==="undefined"){return 1;}else{if(img.currentSrc.indexOf("2x")!=-1){return 2;}else if(img.currentSrc.indexOf("3x")!=-1){return 3;}}}
return 1;}
function animate(state,timeDiff,image,description){var canvasName=(state.tile.memberName_!=undefined?state.tile.memberName_+(state.tile.bit_==null?"":"0x"+state.tile.bit_.toString(16)):state.tile.num);if($('#tilesCanvas_'+canvasName).length==0)
return;var canvas=$('#tilesCanvas_'+canvasName)[0];const canvasOrgWidth=parseInt(canvas.style.width);const canvasOrgHeight=parseInt(canvas.style.height)
var context=canvas.getContext("2d");var frameSizeFactor=getFrameSizeDensityFactor(image);if(state.tile.memberName_!=undefined){var param=getRegParamIfExists(state.tile.memberName_,state.tile.bit_,description);}else{if(state.tile.etindex!=undefined&&state.tile.etindex<tiles_params.length){var tile_params=tiles_params[state.tile.etindex]
var pval="---";var punit="";if(tile_params[0]!=null){tile_params=tile_params[0]
if(tile_params[0].length>1){pval=tile_params[0][0]
punit=getParamUnitStr(tile_params[0][1])}else if(tile_params[0].length==1){pval=tile_params[0][0]}
if(tile_params[0].length>2&&tile_params[0][2]==1){pval=getETtilesParamTranslation(state.tile.etindex+1,pval)}}
var param=new Param(pval,pval,punit,null);}else{var param=new Param();}}
if(!isNaN(param.val)){var speed=param.val/MAX_ANIMATION_VALUE*MAX_FRAME_SEED;var frameTime=1/speed;state.timeDiff+=timeDiff;if(state.timeDiff>frameTime){state.frameNo+=1;state.timeDiff%=frameTime;}
state.frameNo%=state.frames;}
context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);var animw=tiles_canvas_iconw;var propfactor=state.frameWidth/state.frameHeight;var animh=animw/propfactor
var startWidth=(tiles_canvas_iconw-animw)/2
context.drawImage(image,state.frameNo*state.frameWidth*frameSizeFactor,0,state.frameWidth*frameSizeFactor,state.frameHeight*frameSizeFactor,startWidth,0.5*canvasOrgHeight-animh/1.5,animw,animh);drawCanvasFullAreaValue(canvas,(param.val!=null&&state.valueint!=undefined&&state.valueint)?Math.round(param.val):param.str,param.getParamUnit(),null,(state.label!=undefined)?state.label:null,false,'#000000','#000000',0,'#d5d5d5');if($(canvas).parent().hasClass('tiledisabled')){disabledTileEffect(canvas);}}
function updateLevel(tile){if($('#tilesCanvas_'+tile.memberName_).length==0)
return;var canvas=$('#tilesCanvas_'+tile.memberName_)[0];const canvasOrgWidth=parseInt(canvas.style.width);const canvasOrgHeight=parseInt(canvas.style.height)
var context=canvas.getContext("2d");context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);var param=getRegParamIfExists(tile.memberName_);context.strokeStyle="#51507a";context.beginPath();context.lineWidth="2";context.arc(0.07*canvasOrgWidth,0.33*canvasOrgHeight,0.02*canvasOrgHeight,Math.PI,1.50*Math.PI);context.arc(0.17*canvasOrgWidth,0.33*canvasOrgHeight,0.02*canvasOrgHeight,-0.5*Math.PI,0);context.arc(0.17*canvasOrgWidth,0.63*canvasOrgHeight,0.02*canvasOrgHeight,0,0.5*Math.PI);context.arc(0.07*canvasOrgWidth,0.63*canvasOrgHeight,0.02*canvasOrgHeight,0.5*Math.PI,Math.PI);context.closePath();context.stroke();var height=param.val*canvasOrgHeight/100;if(height>canvasOrgHeight){height=canvasOrgHeight;}
if(height>0){context.fillStyle="rgb(81, 80, 122)";context.beginPath();context.arc(0.07*canvasOrgWidth,0.63*canvasOrgHeight-0.3*height,0.005*canvasOrgHeight,Math.PI,1.50*Math.PI);context.arc(0.17*canvasOrgWidth,0.63*canvasOrgHeight-0.3*height,0.005*canvasOrgHeight,-0.5*Math.PI,0);context.arc(0.17*canvasOrgWidth,0.63*canvasOrgHeight,0.005*canvasOrgHeight,0,0.5*Math.PI);context.arc(0.07*canvasOrgWidth,0.63*canvasOrgHeight,0.005*canvasOrgHeight,0.5*Math.PI,Math.PI);context.closePath();context.fill();}
context.beginPath();context.lineWidth="2";context.moveTo(0.07*canvasOrgWidth,0.41*canvasOrgHeight);context.lineTo(0.09*canvasOrgWidth,0.41*canvasOrgHeight);context.moveTo(0.07*canvasOrgWidth,0.555*canvasOrgHeight);context.lineTo(0.09*canvasOrgWidth,0.555*canvasOrgHeight);context.stroke();context.beginPath();context.lineWidth="2";context.moveTo(0.07*canvasOrgWidth,0.335*canvasOrgHeight);context.lineTo(0.1*canvasOrgWidth,0.335*canvasOrgHeight);context.moveTo(0.07*canvasOrgWidth,0.480*canvasOrgHeight);context.lineTo(0.1*canvasOrgWidth,0.480*canvasOrgHeight);context.moveTo(0.07*canvasOrgWidth,0.63*canvasOrgHeight);context.lineTo(0.1*canvasOrgWidth,0.63*canvasOrgHeight);context.stroke();if(param.val>100){drawCanvasFullAreaValue(canvas,'CAL',"",null,null,false,'#000000','#000000',0,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,param.val,param.getParamUnit(),null,"fuelLevellabel",false,'#000000','#000000',0,'#d5d5d5');}}
function updateVersions(softVersion,moduleASoftVer,moduleBSoftVer,moduleCSoftVer,moduleLambdaSoftVer,moduleEcoSTERSoftVer,modulePanelSoftVer){$('#lbSettingsSoftVerCurr').text(softVersion);updateModulesVersions(moduleASoftVer,moduleBSoftVer,moduleCSoftVer,moduleLambdaSoftVer,moduleEcoSTERSoftVer,modulePanelSoftVer);}
function updateThermWave(tile){updateTherm(tile,false);if((controller.type_!=ECOMAX_850i_TYPE)&&tile.extra_&&regParams[tile.extra_.tempSelection]&&regParams[tile.extra_.tempSelection].val){var canvas=document.getElementById("tilesCanvas_"+tile.memberName_);var context=canvas.getContext("2d");if(!canvas.parentElement.classList.contains("tiledisabled")){var img=new Image;img.src=wavePict;try{var side=canvas.style.width*0.07;context.drawImage(img,tiles_canvas_innerw,(canvas.height*0.5)-2*side,side,side);}catch(err){txt="There was an error on this page.\n\n";txt+="Error description: "+err.message+"\n\n";txt+="Click OK to continue.\n\n";console.log(txt);}}}
updateTileModeIcon(tile)}
function getParamUnitStr(unit){if(ETunits!=null&&unit in ETunits){if(ETunits[unit]instanceof Array){if(ETlangNum<ETunits[unit].length){return ETunits[unit][ETlangNum]!="_"?ETunits[unit][ETlangNum].split('%%').join('%'):ETunits[unit][0].split('%%').join('%');}else{return ETunits[unit][0].split('%%').join('%');}}else{return ETunits[unit].split('%%').join('%')}}
return""}
function updateTherm(tile,readOnly){const tileName=(tile.memberName_!=null?tile.memberName_:tile.num);if($("#tilesCanvas_"+tileName).length==0)
return;var canvas=document.getElementById("tilesCanvas_"+tileName);var context=canvas.getContext("2d");if(tile.etindex!=undefined&&tile.etindex<tiles_params.length){var tile_params=tiles_params[tile.etindex]
var pval="---";var punit="";if(tile_params[0]!=null&&tile_params[1]){var tile_paramsdata=tile_params[0]
if(tile_paramsdata[0].length>1){pval=tile_paramsdata[0][0]
punit=getParamUnitStr(tile_paramsdata[0][1])}else if(tile_paramsdata[0].length==1){pval=tile_paramsdata[0][0]}}
var param=new Param(parseFloat(pval),pval,punit,null);if((tile_params.length==5&&tile_params[4]==null)||(tile_params.length==7&&tile_params[6]==null)){readOnly=true;}else{var psetval="---";var psetunit="";if(tile_params[3]!=null){var tile_paramsdata=tile_params[3]
if(tile_paramsdata[0].length>1){psetval=tile_paramsdata[0][0]
psetunit=getParamUnitStr(tile_paramsdata[0][1])}else if(tile_paramsdata[0].length==1){psetval=tile_paramsdata[0][0]}
var param_set=new Param(parseFloat(psetval),psetval,psetunit,null);}else{var param_set=null;}}}else{var param=getRegParamIfExists(tile.memberName_);var param_set=getRegParamIfExists(tile.setMemberName_)
if((controller.type_==ECOMAX_850i_TYPE)&&tile.extra_!=undefined&&tile.extra_!=null&&tile.extra_.index!=undefined){var index=tile.extra_.index
mode_param_name=tile.setMemberName_;if(tile.type_==tiles_type_temp_wave&&index!=null&&parameters_current!=null){for(var i=0;i<therm_choice_table.length;i++){var therm_choice=therm_choice_table[i]
if(parameters_current!=null&&therm_choice in parameters_current){if(parameters_current[therm_choice].value.toString()==index){mode_param_name='ecoSterSetTemp'+(i+1)
break;}}}}
param_set=getRegParamIfExists(mode_param_name);}
if(controller.type_==ECOMAX_850i_TYPE){if(tile.memberName_=="mixerTemp1"){if((parameters_current==null)||(parameters_current!=null&&'HANDLING_H_1'in parameters_current&&parameters_current['HANDLING_H_1'].value==0)){param=new Param();}}
updateTileModeIcon(tile)}
readOnly=readOnly||tile.setMemberName_==tile.memberName_;}
if(param===undefined)
return;context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);if(!readOnly){if(controller.type_==ECOMAX_850i_TYPE&&param_set.val==0){drawCanvasFullAreaValue(canvas,'OFF',null,null,null,false,'#000000','#000000',0,'#d5d5d5');}else{if(param_set!=null){if(controller.type_==ECOMAX_850i_TYPE){drawCanvasFullAreaValue(canvas,param_set.str,param_set.getParamUnit(),"tempfull_tilicon","tempSetTlabel",false,'#000000','#000000',1,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,param_set.str,param_set.getParamUnit(),"tempfulled_tilicon","tempSetTlabel",true,'#000000','#31c1dc',1,'#d5d5d5');}
drawCanvasFullAreaValue(canvas,param.str,param.getParamUnit(),"tempfull_tilicon","tempActTlabel",false,'#000000','#000000',2,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,param.str,param.getParamUnit(),"tempfulled_tilicon","tempActTlabel",true,'#000000','#31c1dc',0,'#d5d5d5');}}}else{if((param_set==null)||(tile.setMemberName_==null)||(controller.protocol_type!='em')||(tile.setMemberName_==tile.memberName_)){drawCanvasFullAreaValue(canvas,param.str,param.getParamUnit(),"tempfull_tilicon","tempActTlabel",false,'#000000','#000000',0,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,param_set.str,param_set.getParamUnit(),"tempfull_tilicon","tempSetTlabel",false,'#000000','#000000',1,'#d5d5d5');drawCanvasFullAreaValue(canvas,param.str,param.getParamUnit(),"tempfull_tilicon","tempActTlabel",false,'#000000','#000000',2,'#d5d5d5');}}
if($("#tilesCanvas_"+tileName).parent().hasClass("tiledisabled")){disabledTileEffect(canvas);}}
function drawCanvasFullAreaValue(canvas,value,unit,icon,label,edit,defcolor,valcolor,drawtype,hrline,vertcenter,horcenter){switch(drawtype){case 0:var dispTextFactors=[0.3,0.25,0.5,0.2,0.27,0.25,0.99,0.5,0.35,0.02,0.5,0.5,0.22,0.3,0.5,0.5,0,0.98,1,0.98,0.01];break;case 1:var dispTextFactors=[0.3,0.4,0.25,0.2,0.27,0.4,0.99,0.25,0.35,0.12,0.25,0.5,0.22,0.42,0.25,0.5,0,0.48,1,0.48,0.01];break;case 2:var dispTextFactors=[0.3,0.4,0.75,0.2,0.27,0.4,0.99,0.75,0.35,0.12,0.75,0.5,0.22,0.42,0.75,0.5,0,0.98,1,0.98,0.51];break;default:return;}
if(canvas["id"]=="tilesCanvas_totalGain"){if(value!='---'){value+="kWh";}
unit=null;}
var onlyTextDisplay=false;if(unit==null&&icon==null){onlyTextDisplay=true;}else{onlyTextDisplay=false;}
var context=canvas.getContext("2d");context.textAlign="start";var canvasRealHeight=parseInt(canvas.style.height);var canvasRealWidth=parseInt(canvas.style.width);var fontSize=dispTextFactors[0]*canvasRealHeight;var fontConf="normal "+fontSize+"px Lato, sans-serif";context.font=fontConf
var valueWidth=context.measureText(value).width
var valueStartWidth=tiles_canvas_iconw;context.fillStyle=valcolor;if(onlyTextDisplay){var iterCount=0;while(valueWidth>tiles_canvas_innerw&&iterCount<10){var propFactor=valueWidth/tiles_canvas_innerw
fontSize=fontSize/propFactor;context.font="normal "+fontSize+"px Lato, sans-serif";valueWidth=context.measureText(value).width
iterCount++;}
context.fillText(value,canvasRealWidth/2-valueWidth/2,dispTextFactors[2]*canvasRealHeight+dispTextFactors[3]*fontSize);}else{var fullValueWidth=valueWidth;if(unit!=null&&unit!=''){context.font="normal "+dispTextFactors[4]*fontSize+"px Lato, sans-serif";fullValueWidth+=context.measureText(unit).width;context.font=fontConf;}else{var iterCount=0;while(fullValueWidth>tiles_canvas_valuew&&iterCount<10){var propFactor=fullValueWidth/tiles_canvas_valuew
fontSize=fontSize/propFactor;context.font="normal "+fontSize+"px Lato, sans-serif";fullValueWidth=context.measureText(value).width
iterCount++;}}
valueStartWidth=valueStartWidth+(tiles_canvas_valuew-fullValueWidth)/2
context.fillText(value,valueStartWidth,dispTextFactors[2]*canvasRealHeight+dispTextFactors[3]*fontSize);}
if(unit!=null&&unit!=''){context.font="normal "+dispTextFactors[4]*fontSize+"px Lato, sans-serif";context.fillStyle=valcolor;context.fillText(unit,valueStartWidth+valueWidth,dispTextFactors[7]*canvasRealHeight-dispTextFactors[8]*fontSize);}
if(icon!=null){var iconimg=$('#'+icon)[0]
var orgheight=iconimg.height
var orgwidth=iconimg.width
var animh=fontSize;var heightprop=orgwidth/orgheight;var animw=animh*heightprop
var widthStart=(tiles_canvas_iconw-animw)/2
context.drawImage(iconimg,widthStart,dispTextFactors[10]*canvasRealHeight-dispTextFactors[11]*fontSize,animw,animh);}
if(label!=null){context.font="normal "+dispTextFactors[12]*fontSize+"px Lato, sans-serif";context.fillStyle=defcolor;var labelVal=translate(label);if(onlyTextDisplay){var labValueWidth=context.measureText(labelVal).width
context.fillText(labelVal,canvasRealWidth/2-labValueWidth/2,dispTextFactors[14]*canvasRealHeight+dispTextFactors[15]*fontSize);}else{var labelStartWidth=tiles_canvas_iconw+(tiles_canvas_valuew-context.measureText(labelVal).width)/2;context.fillText(labelVal,labelStartWidth,dispTextFactors[14]*canvasRealHeight+dispTextFactors[15]*fontSize);}}
if(hrline!=undefined&&hrline!=null){context.beginPath();context.strokeStyle=hrline;context.lineWidth=1;context.moveTo(dispTextFactors[16]*canvasRealWidth,dispTextFactors[17]*canvasRealHeight);context.lineTo(dispTextFactors[18]*canvasRealWidth,dispTextFactors[19]*canvasRealHeight);context.stroke();}
if(edit!=undefined&&edit!=null){if(edit){var iconimg=$('#tile_edit_icon')[0]}else{var iconimg=$('#tile_ro_icon')[0]}
var orgheight=iconimg.height
var orgwidth=iconimg.width
var heightprop=orgwidth/orgheight;var targw=(tiles_canvas_innerw*0.08)
var targh=targw/heightprop
context.drawImage(iconimg,tiles_canvas_innerw,dispTextFactors[20]*canvasRealHeight,targw,targh);}}
function getMousePos(canvas,evt){var rect=canvas.getBoundingClientRect();return{x:evt.clientX-rect.left,y:evt.clientY-rect.top};}
function updateB3B4Therm(tile,readOnly){if($("#tilesCanvas_"+tile.memberName_).length==0)
return;var canvas=document.getElementById("tilesCanvas_"+tile.memberName_);var context=canvas.getContext("2d");var param=getRegParamIfExists(tile.memberName_);var param_set=getRegParamIfExists(tile.setMemberName_);if(param===undefined)
return;context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);drawCanvasFullAreaValue(canvas,(param.val==true)?translate('heating'):translate('noheating'),null,null,null,false,'#000000','#000000',2,'#d5d5d5');if(!readOnly){if(param_set.val==0){drawCanvasFullAreaValue(canvas,'OFF',null,null,null,false,'#000000','#000000',1,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,param_set.str,param_set.getParamUnit(),"tempfull_tilicon",null,false,'#000000','#000000',1,'#d5d5d5');}}
if($("#tilesCanvas_"+tile.memberName_).parent().hasClass("tiledisabled")){disabledTileEffect(canvas);}}
function getBoilerPowerParam(){var powerKW=getRegParamIfExists("boilerPowerKW");var powerPercent=getRegParamIfExists("boilerPower");if(powerKW.val==null&&powerPercent.val!=null){return powerPercent;}else{return powerKW;}}
function updatePower(tile){var canvas=document.getElementById("tilesCanvas_"+tile.memberName_);const canvasOrgWidth=parseInt(canvas.style.width);const canvasOrgHeight=parseInt(canvas.style.height)
var context=canvas.getContext("2d");var param=getBoilerPowerParam();context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);var radius=canvasOrgWidth/9.5;var fromX=1.05*radius;var fromY=canvasOrgHeight*0.5;context.lineWidth=3;context.strokeStyle='#51507a';context.beginPath();context.arc(fromX,fromY,radius,0,Math.PI,true);context.stroke();var percentValue=param.val/tile.maxValue_;var fillColor="#51507a";context.lineWidth=2;context.strokeStyle=fillColor;var angle=percentValue*(Math.PI)+Math.PI;var horizontal=0.8*radius*Math.cos(angle);var vertical=0.8*radius*Math.sin(angle);var toX=horizontal+fromX;var toY=vertical+fromY;var midpointx=0.3*(toX-fromX)
var midpointy=0.3*(toY-fromY)
context.beginPath();context.moveTo(fromX,fromY);context.lineTo(toX,toY);context.stroke();drawCanvasFullAreaValue(canvas,param.str,param.getParamUnit(),null,null,false,'#000000','#000000',0,'#d5d5d5');}
function updateText(tile){var tileName=(tile.memberName_!=null?tile.memberName_:tile.num);var canvas=document.getElementById("tilesCanvas_"+tileName);if(canvas){var context=canvas.getContext("2d");context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);if(tile.etindex!=undefined&&tile.etindex<tiles_params.length){var tile_params=tiles_params[tile.etindex]
var pvalue="---";if(tile_params[0]!=null&&tile_params[1]){pvalue=parseTileValueArray(tile_params[0],tile.etindex+1);}
drawCanvasFullAreaValue(canvas,pvalue,null,null,null,false,'#000000','#000000',0,'#d5d5d5');}else{if(tile.memberName_=="mode"){drawCanvasFullAreaValue(canvas,getModeParamIfExists(),null,null,null,true,'#000000','#000000',0,'#d5d5d5');}
else if(tile.memberName_=="H"){drawCanvasFullAreaValue(canvas,(getRegParamIfExists(tile.memberName_).val?translate("on"):translate("off")),null,null,null,false,'#000000','#000000',0,'#d5d5d5');}
else{var param=getRegParamIfExists(tile.memberName_,tile.bit_);drawCanvasFullAreaValue(canvas,param.str,param.getParamUnit(),null,null,false,'#000000','#000000',0,'#d5d5d5');}}
if($("#tilesCanvas_"+tileName).parent().hasClass("tiledisabled")){disabledTileEffect(canvas);}}}
function parseTileValueArray(tile_array,etindex){tile_array=tile_array[0]
var pval="---";var punit="";if(tile_array.length>1){pval=tile_array[0]
punit=getParamUnitStr(tile_array[1])}else if(tile_array.length==1){pval=tile_array[0]}
if(tile_array.length>2&&tile_array[2]==1){pval=getETtilesParamTranslation(etindex,pval)}
return pval+punit;}
function updateTextIcon(tile){var tileName=(tile.memberName_!=null?tile.memberName_:tile.num);var canvas=document.getElementById("tilesCanvas_"+tileName);if(canvas){var context=canvas.getContext("2d");context.fillStyle="#FFFFFF";context.fillRect(0,0,canvas.width,canvas.height);var currParam=getRegParamIfExists("lambdaLevel")
var setParam=getRegParamIfExists("lambdaSet");var statusParam=getRegParamIfExists("lambdaStatus");var currVal=null;var setVal=null;if(tile.memberName_=="lambdaLevel"){var canvasRealHeight=parseInt(canvas.style.height);var canvasRealWidth=parseInt(canvas.style.width);var fontSize=0.23*canvasRealHeight;var widthStart=tiles_canvas_iconw*0.15
context.font="normal "+fontSize+"px Lato, sans-serif";var otextw=context.measureText("O").width;context.fillText("O",widthStart,0.79*canvasRealHeight);fontSize=0.1*canvasRealHeight;context.font="normal "+fontSize+"px Lato, sans-serif";context.fillText("2",widthStart+otextw*0.92,0.81*canvasRealHeight);if(setParam.val==25.5)
setVal=NAN_REPR;else
setVal=setParam.str;if(statusParam.val==0)
currVal=translate("lambda_stop");else if(statusParam.val==1)
currVal=translate("lambda_start");else
currVal=currParam.str;}
if(setVal!=null){var val=parseFloat(setVal);if(!isNaN(val)&&setParam!=null){drawCanvasFullAreaValue(canvas,setParam.str,setParam.getParamUnit(),null,null,false,'#000000','#000000',1,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,setVal,"",null,null,false,'#000000','#000000',1,'#d5d5d5');}
val=parseFloat(currVal);if(!isNaN(val)&&currParam!=null){drawCanvasFullAreaValue(canvas,currParam.str,currParam.getParamUnit(),null,null,false,'#000000','#000000',2,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,currVal,"",null,null,false,'#000000','#000000',2,'#d5d5d5');}}else{if(currVal!=null){var val=parseFloat(currVal);if(isNaN(val)&&currParam!=null){drawCanvasFullAreaValue(canvas,currParam.str,currParam.getParamUnit(),null,null,false,'#000000','#000000',0,'#d5d5d5');}else{drawCanvasFullAreaValue(canvas,currVal,"",null,null,false,'#000000','#000000',0,'#d5d5d5');}}}}}
function updateB2(tile){updateTherm(tile,false);updateTileModeIcon(tile)}
function updateTileModeIcon(tile){if(tile.extra_&&tile.extra_.addParameters&&parameters_current!=null){var add_params=tile.extra_.addParameters.split(';')
var index=tile.extra_.index
var mode_param=null
if((controller.type_==ECOMAX_850i_TYPE)&&tile.type_==tiles_type_temp_wave&&index!=undefined&&index!=null){for(var i=0;i<therm_choice_table.length;i++){var therm_choice=therm_choice_table[i]
if(parameters_current!=null&&therm_choice in parameters_current){if(parameters_current[therm_choice].value.toString()==index){mode_param=STER_MODE_PARAM[controller.type_]+(i+1)
break;}}}}else if(THERM_MODE_EDIT_TILES.length==OTHER_MODE_EDITS.length&&THERM_MODE_EDIT_TILES.indexOf(tile.memberName_)!=-1){mode_param=OTHER_MODE_EDITS[THERM_MODE_EDIT_TILES.indexOf(tile.memberName_)]}else{for(var i=0;i<add_params.length;i++){if(add_params[i].indexOf(STER_MODE_PARAM[controller.type_])!=-1){mode_param=add_params[i];break;}}}
if(mode_param!=null&&parameters_current[mode_param]){PARAMETERS_CONN_DYNAMIC_CONN[tile.memberName_]=mode_param
var mode_num=parameters_current[mode_param].value
if(mode_num>=0&&mode_num<STER_MODES_IMGS_ICONS[controller.type_].length){var tileObj=$('#tilesFooter_'+tile.memberName_).find('.tileHeaderRight');if(tileObj.length>0){var link=$("<a>");link.attr("href","javascript:;");link.attr("class","tileModeLink");link.attr("style","line-height: "+(tiles_canvas_headerh-2)+"px")
if(controller.type_==ECOMAX_850i_TYPE){link.attr("onclick","popupModeOnlyParam('"+tile.memberName_+"')");}else{link.attr("onclick","popupModeEditParam('"+tile.memberName_+"')");}
var whint=parseInt(TILES_MODE_ICON_WPROC*tiles_canvas_headerh);link.html('<i class="tileIconCommon" style="height: '+whint+'px; width: '+whint+'px; background-size: '+TILES_ICON_WHPROP*TILES_ICON_MULTIPLIERW*whint+'px '+TILES_ICON_MULTIPLIERH*whint+'px; background-position: '+STER_MODES_IMGS_ICONS[controller.type_][mode_num][0]*whint*TILES_ICON_WHPROPOFF+'px '+STER_MODES_IMGS_ICONS[controller.type_][mode_num][1]*whint+'px;"></i>')
tileObj.html(link);}}}}}
function updateB3B4(tile){updateB3B4Therm(tile,false);updateTileModeIcon(tile)}
function tilesStopAnimation(){tiles_stop_animation=true;}
function tilesStartAnimation(){tiles_stop_animation=false;if(!tiles_animation_run){var date=new Date();contentAnimate(date.getTime());}}
function disableTile(paramName){$('[id^="tilesCanvas_'+paramName+'"]').each(function(){if(!disableTileMode){$(this).parent().addClass('tiledisabled');$(this).removeClass('tilebutton');disabledTileEffect(this);}else{$(this).parent().addClass('tilemodedisabled');}});}
function enableTile(paramName){$('[id^="tilesCanvas_'+paramName+'"]').each(function(){if($(this).parent().hasClass('tilemodedisabled')){$(this).parent().removeClass('tilemodedisabled');}else{$(this).parent().removeClass("tiledisabled");$(this).addClass('tilebutton');}});delete changedParams.paramName;}
function disabledTileEffect(canvas){var context=canvas.getContext("2d");context.fillStyle='rgba(255,255,255,0.65)';context.fillRect(0,0,canvas.width,canvas.height);}
function getTileParamName(paramName){if(!$.isEmptyObject(tiles_params)){var tiles_ids_array=[];$.each(tiles_dict,function(key,value){if(value.edname==paramName){tiles_ids_array.push(value.etindex);}});return tiles_ids_array;}
for(var tileName in PARAMETERS_CONN_DYNAMIC_CONN){if(paramName==PARAMETERS_CONN_DYNAMIC_CONN[tileName]){return tileName;}}
for(var tileName in PARAMETERS_CONN){for(var item=0;item<PARAMETERS_CONN[tileName].length;item+=1){if(paramName==PARAMETERS_CONN[tileName][item]){return tileName;}}}
return paramName;}
function getTileParamNameByKey(paramKey){for(var tileName in RM_PARAMETERS_CONN){if(paramKey==RM_PARAMETERS_CONN[tileName]){return tileName;}}
return null;}
function addTileGm(tile){var name=tile.memberName_
+(tile.bit_==null?"":"0x"+tile.bit_.toString(16));var type=tile.type_;if(tile.setMemberName_!=null){PARAMETERS_CONN[name]=[tile.setMemberName_];}
addTile(tile,type);var clickable=type==tiles_type_temp;if(!$.isEmptyObject(ETparametersData)){var param_ind=getEtParamIndex(tile.setMemberName_);if(param_ind!=undefined){var popupMethod='popupParamETeditableTile('+param_ind+',null,\''+tile.memberName_+'\',\''+findEditableParamNum(param_ind)+'\');';}else{var popupMethod='';}}else{var popupMethod='popupParam(\''+tile.memberName_+'\',\''+""+'\',\''+false+'\',\''+tile.memberName_+'\');"';}
return getTileString(name,name,clickable,popupMethod,false,false,false,(tile.extra_&&tile.extra_.addParameters));}
function createTilesGm(tab){var new_dict={};rebuildEditableParameters=false;tiles_tab=tab;cleanTiles();var current_tiles=[];var tilesString='';for(t in tab){current_tiles.push(tab[t].memberName_);tilesString+=addTileGm(tab[t]);if(tiles_dict.hasOwnProperty(tab[t].memberName_)&&tiles_dict[tab[t].memberName_].name_!=tab[t].name_)
rebuildEditableParameters=true;var tabName=tab[t].memberName_
+(tab[t].bit_==undefined?'':"0x"
+tab[t].bit_.toString(16));new_dict[tabName]=tab[t];}
var tilesDiv=document.getElementById('tilesMain');tilesDiv.innerHTML=tilesString;tiles_dict=new_dict;if(rebuildEditableParameters)
cleanParameters();setCanvasResParams();updateStatic();translateTilesHeaders();return current_tiles;}
function updateStaticGm(){for(var i in tiles_temp){if(!tiles_temp[i].close)
updateTherm(tiles_temp[i]);}
for(var i in tiles_temp_ro){if(!tiles_temp_ro[i].close)
updateTherm(tiles_temp_ro[i],true);}
for(var i in tiles_temp_wave){if(!tiles_temp_wave[i].close)
updateThermWave(tiles_temp_wave[i]);}
for(var i in tiles_level){if(!tiles_level[i].close)
updateLevel(tiles_level[i]);}
for(var i in tiles_power){if(!tiles_power[i].close)
updatePower(tiles_power[i]);}
for(var i in tiles_text){if(!tiles_text[i].close)
updateText(tiles_text[i]);}
for(var i in tiles_text_icon){if(!tiles_text_icon[i].close)
updateTextIcon(tiles_text_icon[i]);}}
function getEtParamIndex(paramName){if((paramName===null)||(paramName===undefined)){return undefined;}
for(const elem of Object.keys(ETparametersData)){let name=ETparametersData[elem].name;if((name!==undefined)&&(name.indexOf(paramName)!=-1)){return elem;}}
return undefined;}
function tileETparamsChange(){if(tiles_params.length!=new_tiles_params.length)
return true;for(var i=0;i<tiles_params.length;i++){if(tiles_params[i][1]!=new_tiles_params[i][1]){return true;}}
return false;}
function createTilesET(){if(!$.isEmptyObject(tiles_tab)){if(tileETparamsChange(new_tiles_params)||tilesResChange){tiles_params=new_tiles_params;var new_dict={};cleanTiles();var tilesString='';for(var i=0;i<tiles_params.length;i++){if(tiles_params[i][2]){var tile_set=tiles_tab[i];tilesString+=addTileET(i,tile_set);var tabName=i;new_dict[tabName]=tile_set;}}
var tilesDiv=document.getElementById('tilesMain');tilesDiv.innerHTML=tilesString;tiles_dict=new_dict;setCanvasResParams();}
tiles_params=new_tiles_params;updateStatic();translateTilesHeaders();}}
function openEtTileEditPopup(edmode,param,num){popup_title="tiletrans_"+(parseInt(num)+1);if(edmode==0){popupParamETeditable(param);}else if(edmode==1){popupParamETbit(param);}}
function addTileET(num,tile){var type=tile.type;tile.num=tile.etindex=num;tile['close']=false;addTile(tile,type);var clickable=false;var popupMethod=null;var disabled=false;if(changedParams[tile.edname]!=undefined){disabled=true;}
if(tile.etindex<tiles_params.length){var tile_params=tiles_params[tile.etindex];if(tile_params.length==5){if(tile_params[4]!=null){clickable=true;popupMethod='popupParamETeditableTile('+tile_params[4]
+',null,null);';}}else if(tile_params.length>6){var edmode=tile_params[5]
if(edmode!=null){clickable=true;popupMethod='openEtTileEditPopup('+edmode+','+tile_params[6]+','+num+');';}}}
return getTileString(num,num,clickable,popupMethod,true,tile['close'],disabled,(tile.extra_&&tile.extra_.addParameters));}
function addTileEm(tile){var name=tile.memberName_;var header=name;var type=tile.type_;var popup=false;addTile(tile,type);var clickable=popup=(type==tiles_type_temp||type==tiles_type_temp_wave);if(type==tiles_type_text&&name=='mode'){if(tile.extra_!=popup_cannot_control_boiler){clickable=true;popup=true;}
popup_boiler_ctrl=tile.extra_;}
if((type==tiles_type_b2)||(type==tiles_type_b3b4)||((type==tiles_type_temp||type==tiles_type_temp_wave)&&(tile.extra_!=null&&tile.extra_.addParameters!=undefined)&&controller.type_==ECOMAX_850i_TYPE)){var popupMethod=null;clickable=popup=false;}else{var popupMethod='popupParam(\''+name+'\',\'\');';}
return getTileString(name,header,clickable,popupMethod,false,false,false,(tile.extra_&&tile.extra_.addParameters));}
function createTilesEm(tab){var new_dict={};PARAMETERS_CONN_DYNAMIC_CONN={}
tiles_tab=tab;cleanTiles();var current_tiles=[];var tilesString='';for(t in tab){current_tiles.push(tab[t].memberName_);tilesString+=addTileEm(tab[t]);if(tiles_dict.hasOwnProperty(tab[t].memberName_)&&tiles_dict[tab[t].memberName_].name_!=tab[t].name_)
rebuildEditableParameters=true;var tabName=tab[t].memberName_;new_dict[tabName]=tab[t];}
tiles_dict=new_dict;if(rebuildEditableParameters){updater.editableParamsVer_=-1;}
var tilesDiv=document.getElementById('tilesMain');tilesDiv.innerHTML=tilesString;setCanvasResParams();updateStatic();updateTranslations();return current_tiles;}
function updateStaticEm(){for(var i in tiles_temp){updateTherm(tiles_temp[i]);}
for(var i in tiles_temp_ro){updateTherm(tiles_temp_ro[i],true);}
for(var i in tiles_temp_wave){updateThermWave(tiles_temp_wave[i]);}
for(var i in tiles_level){updateLevel(tiles_level[i]);}
for(var i in tiles_stream){updateStream(tiles_stream[i]);}
for(var i in tiles_power){updatePower(tiles_power[i]);}
for(var i in tiles_text){updateText(tiles_text[i]);}
for(var i in tiles_text_icon){updateTextIcon(tiles_text_icon[i]);}
for(var i in tiles_b2){updateB2(tiles_b2[i]);}
for(var i in tiles_b3b4){updateB3B4(tiles_b3b4[i]);}}
function updateEditConnectedStaticEm(){for(var i in tiles_temp_wave){updateThermWave(tiles_temp_wave[i]);}
for(var i in tiles_temp){updateTherm(tiles_temp[i]);}
for(var i in tiles_b2){updateB2(tiles_b2[i]);}
for(var i in tiles_b3b4){updateB3B4(tiles_b3b4[i]);}}
var SCHEMA_NAN="---";var SCHEMA_NR=1;var PUMP_WORK_COLOR='#00C000';var PUMP_STOP_COLOR='#000000';var DEFAULT_SCHEMA_IMG={};var DEFAULT_SCHEMA_TITLE_PROC=0.11
var DEFAULT_SCHEMA_LABEL_PROC=0.055
var DEF_SCHEMA_LPANEL_LABELS_TRANS=[['#lbSchema_modeLabel','mode'],['#lbSchema_boilerPowerLabel','boilerPower'],['#lbSchema_fuelLevelLabel','fuelLevel'],['#lbSchema_fuelStreamLabel','fuelStream'],['#lbSchema_fanPowerLabel','fanPower'],['#lbSchema_tempOpticalSensorLabel','tempOpticalSensor']];function Schema(pict_directory){this.pictDirectory_=pict_directory;this.protocol_type=undefined;this.img_id=-1;this.controllerID=SCHEMA_NAN;}
function getSchemaFileName(img_id,prefix){var img_id_str=getThreeDigitNumber(img_id);var schema_img=prefix+img_id_str+'.svg';return schema_img;}
function getThreeDigitNumber(num){return(num<100?'0':'')+(num<10?'0':'')+num;}
function isIE(){return((navigator.appName=='Microsoft Internet Explorer')||((navigator.appName=='Netscape')&&(new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent)!=null)));}
function schemaUpdateView(img_id,regType){if(ngp_hide("diag")){return;}
SCHEMA_NR=img_id;schema.protocol_type=controller.protocol_type;if(isDeviceGm3Conf()){PUMP_STOP_COLOR='#C4C4C4';schemaUpdateViewET(img_id,regType);}else if(controller.protocol_type=='em'){PUMP_STOP_COLOR='#000000';schemaUpdateViewEm(img_id,regType);}else if(controller.protocol_type=='gm3'){schemaUpdateViewGm(img_id,regType);}}
function setPumpColor(id,pumpConnected,pumpWorks){var color='';if(pumpConnected&&pumpWorks){color=PUMP_WORK_COLOR;}else{color=PUMP_STOP_COLOR;}
$('#'+id).css('stroke',color);$('#'+id+' polygon').css('fill',color);$('#'+id+' path').css('stroke',color);$('#'+id+' circle').css('stroke',color);if($('#schemaTooltip').length>0){$('#'+id).attr("onmousemove","ShowSchemaTooltip(evt,"+(pumpConnected&&pumpWorks)+")");$('#'+id).attr("onmouseout","HideSchemaTooltip()");$('#'+id+' polygon').attr("onmousemove","ShowSchemaTooltip(evt,"+(pumpConnected&&pumpWorks)+")");$('#'+id+' polygon').attr("onmouseout","HideSchemaTooltip()");}}
function ShowSchemaTooltip(evt,punpon)
{if(punpon){$('#schemaTooltip').text(translate('on'));}else{$('#schemaTooltip').text(translate('off'));}
$('#schemaTooltip').css('left',(evt.clientX+10)+"px");$('#schemaTooltip').css('top',(evt.clientY+18)+"px");$('#schemaTooltip').show()}
function HideSchemaTooltip()
{$('#schemaTooltip').hide()}
function schemaUpdateValues(){if(ngp_hide("diag")){return;}
if(schema.protocol_type===undefined||schema.protocol_type.length==0||schema.protocol_type=="none")
return;if(isDeviceGm3Conf()){schemaUpdateValuesET();}else if(schema.protocol_type=='gm3'){schemaUpdateValuesGm();}else if(schema.protocol_type=='em'){schemaUpdateValuesEm();}
else{console.log('Unknown schema.protocol_type: '+schema.protocol_type+'!');}
updateSchemaTranslation();}
function updateSchemaTranslation(){if(typeof schema=='undefined')
return;if(typeof schema.protocol_type=='undefined')
return;if(schema.protocol_type.length==0||schema.protocol_type=="none")
return;var maxlabelsize=parseInt(DEFAULT_SCHEMA_LABEL_PROC*$('#schemaImg').width())
var labelfsize=parseInt($(DEF_SCHEMA_LPANEL_LABELS_TRANS[0][0]).css('font-size'))
if(!isNaN(labelfsize)){for(var labtr in DEF_SCHEMA_LPANEL_LABELS_TRANS){var labarr=DEF_SCHEMA_LPANEL_LABELS_TRANS[labtr]
var tmplabel=$(labarr[0])
var ltext=translate(labarr[1])
if(ltext.length>18){ltext=ltext.substr(0,16)+"..."}
tmplabel.text(ltext)}}}
function disableParamOnSchema(paramName,value){$("#lbSchema_"+paramName).parent().attr("class","disabled");$("#lbSchema_"+paramName).parent().removeAttr("onclick");$("#lbSchema_"+paramName).parent().children().first().removeAttr("onclick");}
function enableParamOnSchema(paramName,value){$("#lbSchema_"+paramName).parent().attr("onclick",'popupParam("'+paramName+'");');$("#lbSchema_"+paramName).parent().attr("class","hover_group");}
function activateParamsOnSchemaEvents(){$("#schemaImg [onclick*='popupParam']").attr("class","hover_group");}
function setPathColor(name,stroke,fill){$("#"+name).css('stroke',stroke);$("#"+name).css('fill',fill);}
var ECOMAX_SCHEMA_PREFIX='schema_';var DEFAULT_SCHEMA_850P=0;var DEFAULT_SCHEMA_850i=100;DEFAULT_SCHEMA_IMG[ECOMAX_850P_TYPE]=DEFAULT_SCHEMA_850P;DEFAULT_SCHEMA_IMG[ECOMAX_850i_TYPE]=DEFAULT_SCHEMA_850i;var mixerIds=null;var mixerLabelLetters=["A","B","C","D","E","F","G","H"];var schemaToLoadName="";var schemaLoadedName="";function schemaUpdateViewEm(img_id,regType){if((img_id==255)||(img_id===null)){helpers.hide(document.getElementById("tabHrSchema"));return;}
if(schema.img_id!=img_id){schema.img_id=img_id;$("#schemaImg").svg('destroy');$("#schemaImg").svg({onLoad:function(){if(isIE()){$(this).height(650);}
updateSchemaTranslation();setTimeout(schemaUpdateValuesEm,500);},settings:{}});var svg=$("#schemaImg").svg('get');svg.load(schema.pictDirectory_+getSchemaFileName(img_id,ECOMAX_SCHEMA_PREFIX),{addTo:false,changeSize:true},function(){alert("Load was performed.");});addTabToMenu("tabHrSchema");}}
function getServerSchemaResponse(result,textStatus,xmlhttprequest){if(result!=""){var svg=$("#schemaImg").svg('get');svg.add($(result));var svgel=$('#schemaImg').find('svg')[0];svgel.setAttribute('viewBox','0 0 1920 1080');svgel.setAttribute('preserveAspectRatio','xMinYMin meet')
svgel.removeAttribute('width')
svgel.removeAttribute('height')
schemaLoadedName=schemaToLoadName;addTabToMenu("tabHrSchema");$("#schemaInfoLabel").hide();}
else{$("#schemaInfoLabel").show();$("#schemaInfoLabel").text("No image for schema nr "+SCHEMA_NR);}}
function sortedConnectedMixersIds(params){var ids=[];for(var i=0;i<mixerLabelLetters.length;++i){if(params.hasOwnProperty("mixerTemp"+i)&&params["mixerTemp"+i].val!=null&&params.hasOwnProperty("mixerSetTemp"+i)&&params["mixerSetTemp"+i].val!=null){ids.push(i);}}
ids.sort(function(a,b){return a-b;});return ids;}
function sortedConnectedPanels(params){var ids=[];for(var i=0;i<8;++i){var panel_key="ecoSterTemp"+i
if(panel_key in tiles_dict){ids.push(i);}}
return ids;}
function updateSchemaForPanels(ecoSterIds){if(controller.type_==ECOMAX_850i_TYPE){var av_panels_nrs=[];for(var i=0;i<8;++i){if($('#schema_panel'+i).length>0){av_panels_nrs.push(i);$('#schema_panel'+i).hide();}}
for(var i=0;i<ecoSterIds.length;i++){if(i<av_panels_nrs.length){$('#schema_panel'+av_panels_nrs[i]).show();$('#lbSchema_panel'+av_panels_nrs[i]).text(translatePanelName(ecoSterIds[i]));$('#lbSchema_ecoSterTemp'+av_panels_nrs[i]).text(getRegParamIfExists("ecoSterTemp"+ecoSterIds[i]).strWithUnit);}}}
else{$('#lbSchema_ecoSterTemp1').text(getRegParamIfExists("ecoSterTemp1").strWithUnit);}}
var CIRCUIT_NAME_MAX_LEN=14;function updateSchemaForMixer(mixerIdNum,mixerIDLetter){if(controller.type_==ECOMAX_850i_TYPE){schemaIdLabel=mixerIdNum
schemaIdLabel=mixerLabelLetters.indexOf(mixerIDLetter)+1
$('#lbSchema_circuit'+schemaIdLabel+'_LABEL').text('');var circuitName=getCircuitName(mixerIdNum);if(circuitName!=null){if(circuitName.length>CIRCUIT_NAME_MAX_LEN){circuitName=circuitName.slice(0,CIRCUIT_NAME_MAX_LEN-1)+'...';}
$('#lbSchema_circuit'+schemaIdLabel+'_NAME').css('font-size','10px');$('#lbSchema_circuit'+schemaIdLabel+'_NAME').text(circuitName);}}else{$('#lbSchema_mixer'+mixerIDLetter+'Label').text("MIX "+mixerIdNum);}
$('#lbSchema_mixerTemp'+mixerIDLetter).text(getRegParamIfExists("mixerTemp"+mixerIdNum).strWithUnit);$('#lbSchema_mixerTemp'+mixerIDLetter+'Set').text(getRegParamIfExists("mixerSetTemp"+mixerIdNum).strWithUnit);setPumpColor('schema_pumpMixer'+mixerIDLetter,"mixerTemp"+mixerIdNum in regParams,getRegParamIfExists("mixerPumpWorks"+mixerIdNum).val);}
function cleanUnusedMixers(firstMixerNumber){for(var i=firstMixerNumber;i<mixerLabelLetters.length;++i){var mixerIDLetter=mixerLabelLetters[i];$('#lbSchema_mixer'+mixerIDLetter+'Label').text("");$('#lbSchema_mixerTemp'+mixerIDLetter).text(NAN_REPR);$('#lbSchema_mixerTemp'+mixerIDLetter+'Set').text(NAN_REPR);setPumpColor('schema_pumpMixer'+mixerIDLetter,false,false);}}
function schemaUpdateValuesEm(){activateParamsOnSchemaEvents();$('#schemaNumberLabel').hide();$("#schemaInfoLabel").hide();$("#schemaNumberValue").hide();if(getParamValue("ADDITIONAL_MHS")==0&&$("#FIREPLACE").length!=0)
{$("#FIREPLACE").hide();}
if(getRegParamIfExists("contactGZC").val&&getRegParamIfExists("contactGZCActive").val){$('#BOILER').show();}else{$('#BOILER').hide();}
$('#lbSchema_tempCO').text(getRegParamIfExists("tempCO").strWithUnit);$('#lbSchema_tempCOSet').text(getRegParamIfExists("tempCOSet").strWithUnit);$('#lbSchema_tempCWU').text(getRegParamIfExists("tempCWU").strWithUnit);$('#lbSchema_tempCWUSet').text(getRegParamIfExists("tempCWUSet").strWithUnit);$('#lbSchema_tempOpticalSensor').text(getRegParamIfExists("tempOpticalSensor").strWithUnit);$('#lbSchema_fanPower').text(getRegParamIfExists("fanPower").strWithUnit);if(getRegParamIfExists("fuelLevel").val>100){$('#lbSchema_fuelLevel').text("CAL");}
else{$('#lbSchema_fuelLevel').text(getRegParamIfExists("fuelLevel").strWithUnit);}
$('#lbSchema_tempUpperBuffer').text(getRegParamIfExists("tempUpperBuffer").strWithUnit);$('#lbSchema_tempLowerBuffer').text(getRegParamIfExists("tempLowerBuffer").strWithUnit);$('#lbSchema_tempExternalSensor').text(getRegParamIfExists("tempExternalSensor").strWithUnit);$('#lbSchema_tempBack').text(getRegParamIfExists("tempBack").strWithUnit);$('#lbSchema_fuelStream').text(getRegParamIfExists("fuelStream").strWithUnit);$('#lbSchema_tempFeeder').text(getRegParamIfExists("tempFeeder").strWithUnit);$('#lbSchema_tempFlueGas').text(getRegParamIfExists("tempFlueGas").strWithUnit);$('#lbSchema_tempFireplace').text(getRegParamIfExists("tempFireplace").strWithUnit);$('#lbSchema_tempUpperSolar').text(getRegParamIfExists("tempUpperSolar").strWithUnit);$('#lbSchema_tempLowerSolar').text(getRegParamIfExists("tempLowerSolar").strWithUnit);$('#lbSchema_boilerPowerKW').text(getBoilerPowerParam().strWithUnit);var modeVal=getModeParamIfExists();if(modeVal.length>12){modeVal=modeVal.substr(0,11)+"..."}
$('#lbSchema_mode').text(modeVal)
$('#lbSchema_model').text(schema.controllerID);$('#lbSchema_panel1').css('font-size','11px');$('#lbSchema_panel2').css('font-size','11px');$('#lbSchema_panel3').css('font-size','11px');mixerIds=sortedConnectedMixersIds(regParams);if(mixerIds.length>0){for(var i=0;i<mixerIds.length;++i){updateSchemaForMixer(mixerIds[i],(mixerIds[0]>1&&controller.type_==ECOMAX_850i_TYPE)?mixerLabelLetters[i+1]:mixerLabelLetters[i]);}}else{for(var i=0;i<mixerLabelLetters.length;++i){updateSchemaForMixer(i,mixerLabelLetters[i]);}}
cleanUnusedMixers((mixerIds[0]>1&&controller.type_==ECOMAX_850i_TYPE)?mixerIds.length+1:mixerIds.length);updateSchemaForPanels(sortedConnectedPanels(regParams));setPumpColor('schema_pumpCO',getRegParamIfExists("pumpCO").val,getRegParamIfExists("pumpCOWorks").val);setPumpColor('schema_pumpCWU',getRegParamIfExists("pumpCWU").val,getRegParamIfExists("pumpCWUWorks").val);setPumpColor('schema_pumpSolar',getRegParamIfExists("pumpSolar").val,getRegParamIfExists("pumpSolarWorks").val);setPumpColor('schema_pumpCirculation',getRegParamIfExists("pumpCirculation").val,getRegParamIfExists("pumpCirculationWorks").val);setPumpColor('schema_pumpFIREPLACE',getRegParamIfExists("pumpFireplace").val,getRegParamIfExists("pumpFireplaceWorks").val);}
var COLLECTORS_NUMBER=2;function schemaUpdateViewGm(img_id,regType){if(schema.img_id!=img_id){schema.img_id=img_id;$("#schemaImg").svg('destroy');$("#schemaImg").svg({onLoad:function(){if(isIE()){$(this).height(650);}
updateSchemaTranslation();},settings:{}});var svg=$("#schemaImg").svg('get');svg.load(schema.pictDirectory_+getSchemaFileName(img_id,getEcoSolPrefix(schema.controllerID)),{addTo:false,changeSize:true});addTabToMenu("tabHrSchema");}}
function schemaUpdateValuesGm(){$("#schemaNumberValue").text(ENUM_TYPE[106][SCHEMA_NR]);$('#schemaNumberLabel').show();$("#schemaNumberValue").show();$('#schema_T1').text(getRegParamIfExists('T1').strWithUnit);$('#schema_T2').text(getRegParamIfExists('T2').strWithUnit);$('#schema_T3').text(getRegParamIfExists('T3').strWithUnit);$('#schema_T4').text(getRegParamIfExists('T4').strWithUnit);$('#schema_P1').text(getRegParamIfExists('P1').strWithUnit);$('#schema_P2').text(getRegParamIfExists('P2').strWithUnit);$('#schema_H').text(getRegParamIfExists('H').strWithUnit);var collectors=0;if(parameters_current&&'Kolektor_A'in parameters_current)
collectors+=1;if(parameters_current&&'Kolektor_B'in parameters_current)
collectors+=1;for(var i=1;i<=COLLECTORS_NUMBER;++i){var letter='';if(i==1){letter='A';}else if(i==2){letter='B';}else{console.log('schemaUpdateValues: unknown collector number!');}
var param='COLLECTOR_'+letter;if(parameters_current&&param in parameters_current&&parameters_current[param].value!=0){if(parameters_current[param].value==1){$('#Kolektor'+letter+'_1').show();$('#Kolektor'+letter+'_2').hide();}else if(parameters_current[param].value==2){$('#Kolektor'+letter+'_1').hide();$('#Kolektor'+letter+'_2').show();}else{console.log("schemaUpdateValues(): unknown parameter "+param+" value!");}}else{$('#Kolektor'+letter+'_1').hide();$('#Kolektor'+letter+'_2').hide();}}}
var ECOSOL_SCHEMA_PREFIX='ecoSOL300_';var ECOSOL_400500_SCHEMA_PREFIX='ecoSOL400_';var ECOTRONIC_SCHEMA_PREFIX='ecoTRONIC_schemat';var ECOVENT_SCHEMA_PREFIX='ecoVENT_schemat';var ECOMAX360I_SCHEMA_PREFIX='ecoMAX360i_schemat';var SchemaParamsDict={};var SchemaParamsWithSettings={};var SCHEMA_NAME=''
SCHEMAS_PREFIXES_DICT={"ecoTRONIC100":ECOTRONIC_SCHEMA_PREFIX,"ecoTRONIC200":ECOTRONIC_SCHEMA_PREFIX,"ecoVENT":ECOVENT_SCHEMA_PREFIX,"ecoMAX360i":ECOMAX360I_SCHEMA_PREFIX}
function getRegConfDevSchemaFileName(img_id,contrId){if(contrId.indexOf("ecoSOL")!=-1){return getEcoSolPrefix(contrId)+getThreeDigitNumber(img_id)+'.svg';}else if(contrId.indexOf("ecoVENT")!=-1){return;}else{return SCHEMAS_PREFIXES_DICT[contrId]+getThreeDigitNumber(img_id)+"_"+getThreeDigitNumber(clientId)+'.svg';}}
function getRegDevSchemaFileNameVENT(contrId){var exchType=ETparametersData[466].value;return SCHEMAS_PREFIXES_DICT[contrId]+getThreeDigitNumber(exchType)+"_"+getThreeDigitNumber(clientId)+'.svg';}
function getEcoSolPrefix(contrId){if(contrId.indexOf("400")!=-1||contrId.indexOf("500")!=-1||(contrId.indexOf("301")&&[118,226,227,228,229,230,231,232,233,234,235,237,238,239,240,241,242].includes(clientId))){return ECOSOL_400500_SCHEMA_PREFIX;}else{return ECOSOL_SCHEMA_PREFIX;}}
function schemaUpdateViewET(img_id,regType){$('#schemaNumberLabel').hide();if(img_id!=null&&clientId!=null){if(schema.controllerID!=""&&schema.controllerID=="ecoVENT"&&clientId!=null){if(ETparametersData&&ETparametersData[466]!==void 0){var schemaNameVENT=getRegDevSchemaFileNameVENT(schema.controllerID)}else{schemaVentFlag=false;return;}}else if(schema.controllerID==""){return;}else{var schemaName=getRegConfDevSchemaFileName(img_id,schema.controllerID)}
if(schema.img_id!=img_id||schemaNameVENT){schema.img_id=img_id;if(schema.controllerID=="ecoVENT"){SCHEMA_NAME=schemaNameVENT}else{SCHEMA_NAME=schemaName;}
$("#schemaImg").svg('destroy');$("#schemaImg").svg({onLoad:function(){if(isIE()){$(this).height(650);}},settings:{}});var svg=$("#schemaImg").svg('get');if(SCHEMA_NAME!='.svg'){svg.load(schema.pictDirectory_+SCHEMA_NAME,{addTo:false,changeSize:true,onLoad:schemaEcotronicLoaded});}}}}
function schemaEcotronicLoaded(svg,error){if(error!=undefined){removeTabFromMenu("tabHrSchema");$("#schemaInfoLabel").show();$("#schemaInfoLabel").text("No image for schema nr "+SCHEMA_NR);}
else{$('#schemaImg').html($('#schemaImg').html()+'<div id="schemaTooltip" style="display: none;"></div>')
$("#schemaInfoLabel").hide();addTabToMenu("tabHrSchema");translateETschema();}}
function hideSchemaField(id){try{$('#'+id+'data').hide();$('#'+id+'value').hide();$('#'+id+'line').hide();$('#'+id+'bull').hide();$('#'+id+'pict1').hide();$('#'+id+'pict2').hide();$('#'+id+'pict3').hide();$('#'+id+'pict4').hide();$('#'+id+'pict5').hide();resetInitSchemaHidden(id);$('#'+id).hide();}catch(error){console.error("probable schema ID error: ",id);}}
function showSchemaField(id){try{$('#'+id+'data').show();$('#'+id+'value').show();$('#'+id+'line').show();$('#'+id+'bull').show();$('#'+id+'pict1').show();$('#'+id+'pict2').show();$('#'+id+'pict3').show();$('#'+id+'pict4').show();$('#'+id+'pict5').show();resetInitSchemaHidden(id);$('#'+id).show();}catch(error){console.error("probable schema ID error: ",id);}}
function resetInitSchemaHidden(id){var style_attr=$('#'+id).attr('style')
if(style_attr!=undefined&&style_attr.indexOf("visibility:hidden")!=-1){$('#'+id).attr('style','')}}
function setSchemaFieldValue(id,value_array,value_visiblity){if(value_visiblity){value_array=value_array[0];if(value_array.length>1){var unit=getParamUnitStr(value_array[1]);setFieldValue(id,value_array[0]+unit);}else{setFieldValue(id,"---");}}else{setFieldValue(id,"---");}}
function setFieldValue(id,value){if($('#'+id+'value').length>0){$('#'+id+'value').text(value);}else if($('#'+id).length>0&&$('#'+id)[0].tagName.indexOf("text")!=-1){$('#'+id).text(value);}}
function schemaUpdateValuesET(){setPumpColorsEcoTronic();setHeatersColors();setMixerColors();if(!$.isEmptyObject(SchemaParamsWithSettings)){for(var item in SchemaParamsWithSettings){var schema_field=SchemaParamsWithSettings[item];if(schema_field.length==3){if(schema_field[1]){showSchemaField(item);setSchemaFieldValue(item,schema_field[0],schema_field[2]);}else{hideSchemaField(item);}}else{hideSchemaField(item);}}}else{for(var item in SchemaParamsDict){var val=getRegParamIfExists(item).strWithUnit;for(var i=0;i<SchemaParamsDict[item].length;i+=1){if(Array.isArray(SchemaParamsDict[item][i])){$('#'+SchemaParamsDict[item][i][0]).text(val);}else{$('#'+SchemaParamsDict[item][i]).text(val);}}}}}
FonkoPumps={"P1":"CWUCOUT","P3":"H2OUTnum","P4":"H1OUTnum"};GalmetPumps={"P1":"LPOutnum","P2":"LPUpN","P3":"CWUCOUT","P4":"H1OUTnum","P5":"H2OUTnum"};EsnodPumps={"P1":"LPOutnum","P2":"CWUOnum","P3":"CWUCOUT"};ThermoshopPumps={"P1":"LPOutnum","P2":"LPUpN","P3":"CWUCOUT","P4":"H1OUTnum","P5":"H2OUTnum"};PumpsDict={59:FonkoPumps,60:GalmetPumps,62:FonkoPumps,63:GalmetPumps,61:EsnodPumps,96:ThermoshopPumps};FonkoPumpsValues={"P2":["Mod_val4",51]};PumpsDictValues={59:FonkoPumpsValues,62:FonkoPumpsValues};function setPumpColorsEcoTronic(){if(clientId==61){setPumpColorsEcoTronicEsnod();return;}
var outputsStates=getRegParamIfExists("OutState").val;var pumps=PumpsDict[clientId];if(pumps==undefined){pumps={};}
for(var p in pumps){var state=getPompState(getRegParamIfExists(pumps[p]).val,outputsStates);setPumpColor(p,state,state);$("#schema_"+p).text(ENUM_TYPE[0][state?1:0]);}
if(clientId in PumpsDictValues){for(var p in PumpsDictValues[clientId]){var values=PumpsDictValues[clientId][p];var state=getRegParamIfExists(values[0]).val==values[1];setPumpColor(p,state,state);}}}
ESNOD_POMP_OUTPUT_NUM={"P1":4,"P2":0,"P3":7};function setPumpColorsEcoTronicEsnod(){var outputsStates=getRegParamIfExists("BCBOutput").val;for(var p in ESNOD_POMP_OUTPUT_NUM){var state=getPompState(ESNOD_POMP_OUTPUT_NUM[p],outputsStates);setPumpColor(p,state,state);}}
function getPompState(ouputNum,outputsStates){return ouputNum==null?0:(1&(outputsStates>>(ouputNum)));}
HEATERS_ITEMS={"heaterCWU":["CWUST",0x4000],"heaterBuffor":["ASST",0x01]}
MIXER_ITEMS={"mixerH1_2":["CWUST",0x02],"mixerH1_3":["BHST",0x01]}
function setHeatersColors(){for(var p in HEATERS_ITEMS){if(HEATERS_ITEMS[p][0]in regParams&&(regParams[HEATERS_ITEMS[p][0]].val&HEATERS_ITEMS[p][1])==HEATERS_ITEMS[p][1])
setPathColor(p,'#00C000','#00C000');else
setPathColor(p,'#000000','#000000');}}
function setMixerColors(){setPathColor("mixerH1_1",'#00C000','#00C000');for(var p in MIXER_ITEMS){setPathColor(p,'#000000','#FFFFFF');}
for(var p in MIXER_ITEMS){if(MIXER_ITEMS[p][0]in regParams&&(regParams[MIXER_ITEMS[p][0]].val&MIXER_ITEMS[p][1])==MIXER_ITEMS[p][1]){setPathColor(p,'#00C000','#00C000');return;}}}
function translateETschema(){for(var item in SchemaParamsDict){var name=translateParameter(item);name=name.split(" ");for(var label in SchemaParamsDict[item]){var id='';if(Array.isArray(SchemaParamsDict[item][label])){id=SchemaParamsDict[item][label][0]+'label';}else{id=SchemaParamsDict[item][label]+'label';}
var text=$('#'+id);if(text.length>0){var basey=parseInt(text.attr("y"));var basex=parseInt(text.attr("x"));var width=11;text.empty();for(var word=0;word<name.length;word+=1){var tspan=document.createElementNS('http://www.w3.org/2000/svg',"tspan");tspan.setAttribute("sodipodi:role","line");tspan.setAttribute("id",id+word);tspan.setAttribute("y",basey+10*word);tspan.setAttribute("x",basex);text.append(tspan);$('#'+id+word).text(name[word]);var wordWidth=($('#'+id+word).width()==0?name[word].length*4:$('#'+id+word).width());tspan.setAttribute("x",basex+(width-wordWidth)/2);}}}}}