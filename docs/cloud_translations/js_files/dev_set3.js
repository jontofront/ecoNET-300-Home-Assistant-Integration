var EDIT_PARAMS=0;var Parameters={HIDE_CONFIRM_DELAY:1000};var changedParams={};var changedParamsCounters={};var changedParamsUI={};var parameters_current=null;var current_params_edits=null;var rms_l=-1;var rms_r='';var RM_PARAM_NAME_TYPE=0;var RM_KEYPARAM_NAME_TYPE=1;var STANDARD_PARAM_NAME_TYPE=2;var STANDARD_TILEPARAM_NAME_TYPE=3;var ENUM_TYPE={0:['off','on'],1:['off','priority','no_priority','summer_mode'],2:['standard_mode','FuzzyLogic','MinMax'],3:['thermostat_contact','ecoSTER1','ecoSTER2','ecoSTER3'],4:['off','thermostat_contact','ecoSTER1','ecoSTER2','ecoSTER3'],5:['pellet','grate'],6:['off','on_co','on_floor_long','only_pump_long'],7:['off','0:00 - 1:00','1:00 - 2:00','2:00 - 3:00','3:00 - 4:00','4:00 - 5:00','5:00 - 6:00','6:00 - 7:00','7:00 - 8:00','8:00 - 9:00','9:00 - 10:00','10:00 - 11:00','11:00 - 12:00','12:00 - 13:00','13:00 - 14:00','14:00 - 15:00','15:00 - 16:00','16:00 - 17:00','17:00 - 18:00','18:00 - 19:00','19:00 - 20:00','20:00 - 21:00','21:00 - 22:00','22:00 - 23:00','23:00 - 24:00'],8:['off','ecoSTER T1','ecoSTER T2','ecoSTER T3'],9:['auto','auto_eco','day','night','off'],10:['none','boiler_gas','boiler_oil','boiler_pellet','boiler_electric'],11:['none','fireplace','automatic_source'],12:['none','alarms'],13:['no','yes','auto'],14:['fixed_value','weather'],15:['off','on_heaters','on_floor','on_only_pump'],16:['none','room_panel_1','room_panel_2','room_panel_3','room_panel_4','room_panel_5','room_panel_6','room_panel_7','thermostat_terminals_29_30','thermostat_terminals_29_31','thermostat_terminals_26_27_B','thermostat_terminals_28_29_B','thermostat_terminals_26_27_C','thermostat_terminals_28_29_C'],17:['termostat','temperature_correction','correction_and_thermostat'],18:['profile1','profile2','profile3','profile4'],19:['mode_schedule','mode_eco','mode_comfort','mode_outside','mode_airing','mode_party','mode_holiday','mode_antifreez','mode_HUW_loading','mode_off'],20:['standard','PID','PID-C','PID-S'],21:['auto','day','off'],22:['winter','summer','auto'],23:['off','thermostat_contact','ecoSTER1','ecoSTER2','ecoSTER3','off','thermostat_contact','ecoSTER2','ecoSTER3','off','thermostat_contact','ecoSTER3','off','thermostat_contact','ecoSTER1','ecoSTER3','off','ecoSTER1','ecoSTER2','ecoSTER3','off','ecoSTER2','ecoSTER3','off','ecoSTER3','off','ecoSTER1','ecoSTER3','thermostat_contact','thermostat_contact','thermostat_contact','off','off','off'],24:['mode_schedule','night','day','mode_off','mode_airing','mode_heat_now','mode_holiday','mode_antifreez','mode_HUW_loading','mode_off'],100:['user','service','producer'],101:['off','on','schedule'],102:['false','true'],103:['unknown','none','WEP','WPA','WPA2'],104:['','','','off','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],105:['pool','huw'],106:['A','B','C','D','E','F','G','H','I','J','K','L'],107:['right','left'],108:['PL','EN','IT','ES','DA','RO','EL','FR','DE','RU','CZ','PT'],109:['stop','auto','holiday'],110:['1-12','1-15','1.3-20','2-40','5-100'],200:["sunday","monday","thuesday","wednesday","thursday","friday","saturday"]};var ENUM_UNIT=31;var PAR_SECTION_TITLE={};var PARAMETER_UNIT={0:"",1:"°C",2:"s",3:"min",4:"h",5:"d",6:"%",7:"Pa",8:"kPa",9:"bar",10:"kg",11:"kg/h",12:"kcal/kg",13:"kW",14:"kWh/kg",15:"RPM",16:"g",31:"",61:"l/min",62:"kWh",63:"Wh",64:"kWh",65:"kW",67:'kg/m3',68:'J/(kg K)',69:'ms',70:'Hz',71:'m3/h',72:'K',73:'J',74:'ppm',75:'d',76:'L'};var PARAMETERS_INCREASED_BY_2=['LCDJas','LCDKon','Dzwvol'];var PARAMETERS_WITH_NON_ASCII={'Moc_chwilowa':'Moc chwilowa','Uzysk_ca_kowity':'Uzysk całkowity','Nr_fab':'Numer Fab.','Tryb_eco':'Tryb eco','Sch__nocne':'Schł. nocne','Tsch__W_':'Tsch WŁ','Tsch__WY_':'Tsch WYŁ','Alarm_TCOLkr':'Alarm TCOLkr','Kal_T1':'Kal T1','Kal_T2':'Kal T2','Kal_T3':'Kal T3','Kal_T4':'Kal T4','Kol_pr__niowy':'Kol. próżniowy','Poz_detekcji':'Poziom detekcji','Czas_pracy':'Czas pracy','J_zyk':'Język','Kier_enkod':'Kier. enkod.','Szybk_menu':'Szybk. menu','Ambient_light':'Ambient light','Konfig':'Konfiguracja','Alarmy_i_monity':'Alarmy i monity'}
function addNonASCII(name){if(PARAMETERS_WITH_NON_ASCII[name]!=undefined){return PARAMETERS_WITH_NON_ASCII[name];}
return name;}
function fillParSectionTileDic(protocolType){if(protocolType=="em"){PAR_SECTION_TITLE={0:translate('boiler_settings'),2:translate('power_modulation'),4:translate('cwu_settings'),6:translate('mixer')+' 1',7:translate('mixer')+' 2',8:translate('mixer')+' 3',9:translate('mixer')+' 4',10:translate('mixer')+' 5',11:translate('mixer')+' 6',12:translate('mixer')+' 7',13:translate('mixer')+' 8',14:translatePanelSection(1),15:translatePanelSection(2),16:translatePanelSection(3),17:translatePanelSection(4),18:translatePanelSection(5),19:translatePanelSection(6),20:translatePanelSection(7),21:translateCircuitSection(1),22:translateCircuitSection(2),23:translateCircuitSection(3),24:translateCircuitSection(4),25:translateCircuitSection(5),26:translateCircuitSection(6),27:translateCircuitSection(7),30:translate('summer_winter'),35:translate('profil_ecoster'),36:translateEcosterParamsSection(1),37:translateEcosterParamsSection(2),38:translateEcosterParamsSection(3),100:translate('boiler_settings'),101:translate('power_modulation'),102:translate('lighting'),103:translate('stabilization'),104:translate('work'),106:translate('extinction'),108:translate('cleaning'),110:translate('supervision'),111:translate('grate'),112:translate('lambda_probe'),113:translate('external_feeder'),114:translate('cwu'),116:translate('CIRCULATION_PUMP_ECOMAX'),118:translate('buffer'),120:translate('mixer')+' 1',121:translate('mixer')+' 2',122:translate('mixer')+' 3',123:translate('mixer')+' 4',124:translate('mixer')+' 5',125:translate('mixer')+' 6',126:translate('mixer')+' 7',127:translate('mixer')+' 8',130:translatePanelSection(1),131:translatePanelSection(2),132:translatePanelSection(3),133:translatePanelSection(4),134:translatePanelSection(5),135:translatePanelSection(6),136:translatePanelSection(7),140:translateCircuitSection(1),141:translateCircuitSection(2),142:translateCircuitSection(3),143:translateCircuitSection(4),144:translateCircuitSection(5),145:translateCircuitSection(6),146:translateCircuitSection(7),150:translate('system'),152:translate('solar')}}}
MAX_USER_SECTION_NUMBER=100;COLLAPSE_PANEL_TIME=120;function areEqualParamsDict(dict1,dict2){var keys1=Object.keys(dict1);var keys2=Object.keys(dict2);if(keys1.length!=keys2.length)
return false;for(var i in dict1){var p1=dict1[i];var p2=dict2[i];if(p1==undefined||p2==undefined||p1.sec!=p2.sec||p1.pos!=p2.pos||p1.unit!=p2.unit)
return false;}
return true;}
function areEqualLengths(array1,array2){if(array1.length==array2.length){return true;}
return false;}
function getNumberPrecision(n){var precision=0;n=(n+"").split(".");if(n.length>1)
precision=n[1].length;return precision;}
function getParamValue(paramName,unit,mult){if(parameters_current==null||!(paramName in parameters_current)){return null;}
var value=parameters_current[paramName].value;if(isDeviceGm3Conf()){if(value!=undefined&&mult==0.1){value=value.toFixed(1);}
return value;}
if(value==null||value==SENSOR_DISCONNECTED){value=NAN_REPR;}else if(unit==ENUM_UNIT){if(typeof value=='boolean')
value=value?1:0;value=translate(ENUM_TYPE[mult][value]);}else{var precision=getNumberPrecision(mult);if(precision>0){value=value.toFixed(precision+2);value=value.substring(0,value.length-2);}}
return value;}
function getValueBit(value,bit){return((value&bit)>0?1:0);}
function setParameters(params,version,type){if(type==EDIT_PARAMS){if(params!=null){var recreate=false;if(parameters_current==null||!areEqualParamsDict(parameters_current,params)||rebuildEditableParameters){parameters_current=params;rebuildEditableParameters=false;if(controller.protocol_type=="em"&&rebuildEditableParameters){cleanParameters();}
updateParametersView();}else{parameters_current=params;for(var i in parameters_current){var value=getParamValue(i,parameters_current[i].unit,parameters_current[i].mult);if((parameters_current[i].offvalue!==undefined)&&(value==parameters_current[i].offvalue)){$('#lbEditParamValue'+i).text(translate('0'));$('#lbEditParamUnit'+i).text('')}else{if(parameters_current[i].unit==ENUM_UNIT){$('#lbEditParamValue'+i).text(value);value=parameters_current[i].value;}else{$('#lbEditParamValue'+i).text(value);$('#lbEditParamUnit'+i).text(PARAMETER_UNIT[parameters_current[i].unit]);}}}}
updater.editableParamsVer_=version;}else{if(parameters_current==null){cleanParameters();}else{parameters_current=null;updateParametersView();}}}else{setParametersRM(params,version,type);}
translateTabs();}
function getEditParamsResponse(result,textStatus,xmlhttprequest){if(result==null){return;}
if(result.funcdata!=undefined){regConfig=true;}
if(isDeviceGm3Conf()){if(result.confDone==false){confDownloadError();}
if(result.confDone==true){confDownloadSuccess();}
if(result.data!=null){setNewParametersStructureET(result.data,result.sections,result.editableParams,result.informationParams,result.choiceParams,result.buttons,result.serviceMenus,result.configEditableParams,result.configEditableParamsMulti,result.onOffGraph);}
if(controller.protocol_type=="gm3"&&result.funcdata!=undefined){parameters_current=result.funcdata;if("Alarmy_i_monity"in parameters_current){showEcoSolAlarms(parameters_current["Alarmy_i_monity"].value);}}else{updateETSchedule();}
updater.editableParamsVer_=(result&&result.editableParamsVer)?result.editableParamsVer:'0';}else{if(result.data!=null&&Object.keys(result.data).length>0){if(result.remoteMenu!=undefined){remoteMenu=result.remoteMenu}
setParameters(result.data,result.editableParamsVer,EDIT_PARAMS);if(controller.protocol_type=="gm3"&&"Alarmy_i_monity"in result.data){showEcoSolAlarms(result.data["Alarmy_i_monity"].value);}}else{setParameters(result.data,(result&&result.editableParamsVer)?result.editableParamsVer:'0',EDIT_PARAMS);}}
var enableAnything=false;if(result.confirmed!=undefined&&result.confirmed.constructor==Array){for(var i=0;i<result.confirmed.length;i+=1){enableParamEditing(result.confirmed[i]);enableAnything=true;}}
if(enableAnything){updateStatic();}}
function getCurrentParamsEditsResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null){if(Object.keys(result.data).length==0){current_params_edits=null;}
current_params_edits=result.data;updater.currParamsEditsVer_=result.currentDataParamsEditsVer}}
function parseParamName(param){var index=param.indexOf("_");if(index>-1)
return param.slice(index+1,param.length);else
return param;}
function cleanParameters(){$('#userParams').children().remove();$('#serviceParams').children().remove();$("[id^='sectionHeader_']").remove();$("[id^='table_']").remove();}
function isUserParamSection(s){return s<MAX_USER_SECTION_NUMBER;}
function isServiceSection(sec){return $("#serviceParams #sectionHeader_"+sec).length!=0;}
function toggleSection(event){if(event.target&&$(event.target).hasClass("sectionHeader")){var index=event.target.id.substr(14);$('#table_'+index).slideToggle('slow');if($(event.target).hasClass("extended")){$(event.target).removeClass("extended");}else{$(event.target).addClass("extended");}}}
function addCollapsiblePanel(menu){if($('#'+menu+' .sectionHeader').length>1||($('#'+menu+' .sectionHeader').length==1&&$('#'+menu).children().length>2)||(remoteMenu&&$('#'+menu+' .sectionHeader').length>0)){$("#"+menu+" [id^='table_']").hide();$("#"+menu+" [id^='sectionHeader_']").removeClass("extended");document.getElementById(menu).removeEventListener('click',toggleSection);document.getElementById(menu).addEventListener('click',toggleSection);}
if($('#'+menu).children().length==1){$($('#'+menu).children()[0]).show();}}
function addCollapsiblePanels(){if(!ngp_hide("menu_user")){addCollapsiblePanel("userParams");}
addCollapsiblePanel("serviceParams");$("div[id^='serviceParamsET']").each(function(){addCollapsiblePanel($(this).attr("id"));});}
function checkForEmptySections(tables){var emptySection=false;var sections=$('[id^="sectionTable_"]');for(var i=0;i<sections.length;i+=1){var index=parseInt(sections[i].id.split("_")[1]);emptySection|=tables[index]==null||$("#sectionHeader_"+index).text()=="undefined";}
return emptySection;}
function addParamRow(name,pos,sec,value,value_unit,tables,bit){if(tables[sec]!=undefined){var title=document.getElementsByTagName("title")[0].innerHTML;var is_econet=(title==="EcoNet");var onclickFuncStr='';var paramName=name
+(bit==null?"":"0x"+(parseInt(bit)).toString(16));if(!isUserParamSection(sec)&&is_econet){onclickFuncStr='"showPasswordPrompt(\''+name+'\',\''
+paramName+'\''
+(bit==null?'':',\''+bit+'\'')+');"';}else{onclickFuncStr='"popupParam(\''+name+'\',\''+paramName
+'\''+(bit==null?'':',\''+bit+'\'')+');"';}
leftMarginText='';if(controller.protocol_type=="gm3"&&!regConfig){if(parameters_current[name].origName!=null)
leftMarginText=parameters_current[name].origName;else
leftMarginText=name;}else{if(isDeviceGm3Conf()){leftMarginText=parameters_current[name].num;}}
tables[sec][pos]='<tr class="two'
+(parameters_current[name].edit?' click" onclick='
+onclickFuncStr:' disabled"')
+'>'
+'<td class="tdParamsLeftMargin" >'
+leftMarginText
+'</td>'
+'<td class="tdParamsDescr" >'
+'<div id="lbEditParam'
+paramName
+'" class="paramsDescr">'
+translateParameter(paramName)
+'</div></td>'
+'<td class="tdParamsValue" >'
+'<div id="lbEditParamValueUnit'
+paramName
+'" class="paramsValue" '
+'>'
+'<span id="lbEditParamValue'
+paramName
+'" class="innerParamValue">'
+value
+'</span><span id="lbEditParamUnit'
+paramName
+'" class="innerParamUnit">'
+value_unit
+'</span></div></td>'
+'<td class="tdParamsEdtype '
+(parameters_current[name].edit?'paramEditIco':'paramViewIco')+'" ><i class="paramRowIcon"></i></td>'+
'</tr>';}}
function parentAction(element_id){$('#'+element_id).trigger("click");}
function updateParametersView(){$('.tableParamsSection').empty();$('#userParamsErr').hide();$('#serviceParamsErr').hide();if(parameters_current!=null){var tables=[];var userSections=0;var serviceSections=0;var newSection=false;for(var i in parameters_current){var value=getParamValue(i,parameters_current[i].unit,parameters_current[i].mult);var value_unit=translate(PARAMETER_UNIT[parameters_current[i].unit]);if((parameters_current[i].offvalue!==undefined)&&(value==parameters_current[i].offvalue)){value=translate('0');value_unit='';}
var sec=parameters_current[i].sec;var pos=parameters_current[i].pos;if(tables[sec]===undefined&&sec!=254){tables[sec]=[];if(isUserParamSection(sec))
++userSections;else
++serviceSections;if(!$('#sectionHeader_'+sec).length){newSection=true;}}
addParamRow(i,pos,sec,value,value_unit,tables);if(i in changedParams){enableParamEditing(i);}}
newSection|=checkForEmptySections(tables);fillParSectionTileDic(controller.protocol_type);var singleUserSection=userSections<=1;var singleServiceSection=serviceSections<=1;if(remoteMenu==true){singleUserSection=false;singleServiceSection=false;}
if(newSection){cleanParameters();for(var i in tables){if(isUserParamSection(i)){var header=(singleUserSection?'':'<div id="sectionHeader_'+i
+'" class="sectionHeader"><i class="paramArrIco" onclick="parentAction(\'sectionHeader_'+i+'\');"></i><span onclick="parentAction(\'sectionHeader_'+i+'\');" id="sectionHeaderText_'+i+'">'
+PAR_SECTION_TITLE[i]+'</span></div>')
+'<div id="table_'
+i
+'"><table id="sectionTable_'
+i
+'" class="tableParamsSection"></table></div>';$('#userParams').append(header);}else{var header=(singleServiceSection?'':'<div id="sectionHeader_'+i
+'" class="sectionHeader"><i class="paramArrIco" onclick="parentAction(\'sectionHeader_'+i+'\');"></i><span onclick="parentAction(\'sectionHeader_'+i+'\');" id="sectionHeaderText_'+i+'">'
+PAR_SECTION_TITLE[i]+'</span></div>')
+'<div id="table_'
+i
+'"><table id="sectionTable_'
+i
+'" class="tableParamsSection"></table></div>';$('#serviceParams').append(header);}}
addCollapsiblePanels();}
for(var i in tables){if(tables[i].length>0){var parameters='';var counter=0;for(var p in tables[i]){if(counter%2==0){tables[i][p]=tables[i][p].replace('class="two','class="one');}
parameters+=tables[i][p];++counter;}
$('#sectionTable_'+i).append(parameters);}}}
if($('#rmUserParams').children().length==0&&$('#userParams').children().length==0){$('#userParamsErr').show();}
if(!ngp_hide("menu_service")){if($('#serviceParams').children().length==0){$('#serviceParamsErr').show();}else{addTabToMenu("tabHrServiceParams");}}
if(!ngp_hide("menu_user")&&$('#userParams').children().length!=0){addTabToMenu("tabHrUserParams");}
if($('#rmUserParams').children().length!=0){removeTabFromMenu("tabHrServiceParams");}
updateParametersTranslation();$('#popupPasswdOK').val(translate('ok'));$('#popupPasswdCancel').val(translate('cancel'));$('#popupPasswdDesc').text(translate('enter_password'));}
function isLockElement(index){if(remote_menu_structure!=null&&index<remote_menu_structure.length)
if('lock'in remote_menu_structure[index]){return remote_menu_structure[index].lock}
return false}
function getLockIndex(index){if(remote_menu_structure!=null&&index<remote_menu_structure.length)
if('lock_index'in remote_menu_structure[index]){return remote_menu_structure[index].lock_index}
return 0}
function getQueryStringParameterByName(name,urlString){name=name.replace(/[\[]/, "\\\[").replace(/[\]]/,"\\\]");var regexS="[\\?&]"+name+"=([^&#]*)";var regex=new RegExp(regexS);var results=regex.exec(urlString);if(results==null)
return"";else
return decodeURIComponent(results[1].replace(/\+/g," "));}
function showPasswordPrompt(param,title,bit,paramNum){if(changedParams[param]!=undefined){return;}
if(!checkCurrentDevActive())
return;if(document.getElementById("serviceParamsMain").hasAttribute("data-user-authenticated")){popupParam(param,title,bit,paramNum);}else{$('#paramInfoPasswdPopup').hide();$('#inpServicePasswd').val('');openPopup('askPasswdPopup');$('#askPasswdPopup').attr('data-param-name',param);$('#askPasswdPopup').attr('data-param-title',title);$('#askPasswdPopup').attr('data-param-bit',bit);$('#inpServicePasswd').trigger("focus");}}
function validatePassword(event,validatingFunc){if(event.keyCode!=13){return true;}
validatingFunc();}
function checkServicePassword(){controller.getPassword(checkPassword);}
function getSHA512(text){var shaObj=new jsSHA(text,"TEXT");var hash=shaObj.getHash("SHA-512","HEX");return hash;}
function toFourCharsPassword(value){result=""
if(value.length>0&&value.length<4){zeroCount=4-value.length;for(var i=0;i<zeroCount;i++){result+="0";}}
result+=value;return result}
function checkPassword(result,textStatus,xmlhttprequest){var passwd=toFourCharsPassword($('#inpServicePasswd').val())
if(result.password!=getSHA512(passwd)){$('#paramInfoPasswdPopup').text(translate('wrong_password'));$('#paramInfoPasswdPopup').show();}else{$('#askPasswdPopup').hide();popupParam($('#askPasswdPopup').attr('data-param-name'),$('#askPasswdPopup').attr('data-param-title'),$('#askPasswdPopup').attr('data-param-bit'));document.getElementById("serviceParamsMain").setAttribute("data-user-authenticated","true");}}
function addChangeParamsObj(key,type,value,index){changedParams[key]=(index!=undefined)?{"type":type,"index":index}:{"type":type};}
function disableParam(paramName){if(isDeviceGm3Conf()){$('.'+paramName).each(function(){$(this).addClass('disabled');$(this).removeClass('click');});}else{$('[id^="lbEditParam'+paramName+'"]').each(function(){$(this).parent().parent().addClass('disabled');$(this).parent().parent().removeClass('click');});}}
function enableParam(paramName){if(isDeviceGm3Conf()){$('.'+paramName).each(function(){$(this).removeClass('disabled');$(this).addClass('click');});}else{$('[id^="lbEditParam'+paramName+'"]').each(function(){$(this).parent().parent().removeClass('disabled');$(this).parent().parent().addClass('click');});}}
function disableParamEditing(paramName,value,index){addChangeParamsObj(paramName,STANDARD_PARAM_NAME_TYPE,value,index)
disableParam(paramName);var tileName=getTileParamName(paramName);if(tileName!=null){if(Array.isArray(tileName)){for(edindex in tileName){disableTile(tileName[edindex],value);}
return}
if(tileName in tiles_dict){disableTile(tileName,value);}
if(tileName.substring(0,9)=='mixerTemp'){var mixerId=tileName.replace('mixerTemp','');var mixerLetter=mixerLabelLetters[mixerIds.indexOf(parseInt(mixerId))];tileName='mixerTemp'+mixerLetter;}
if($("#lbSchema_"+tileName).length!=0){disableParamOnSchema(tileName,value);}}}
function enableParamEditing(paramName){enableParam(paramName);tileName=getTileParamName(paramName);if(tileName!=null){if(Array.isArray(tileName)){for(edindex in tileName){enableTile(tileName[edindex]);}
delete changedParams[paramName];return}
if(tileName in tiles_dict){enableTile(tileName);}
if(tileName.substring(0,9)=='mixerTemp'){var mixerId=tileName.replace('mixerTemp','');var mixerLetter=mixerLabelLetters[mixerIds.indexOf(parseInt(mixerId))];tileName='mixerTemp'+mixerLetter;}
if($("#lbSchema_"+tileName).length!=0){enableParamOnSchema(tileName);}}
delete changedParams[paramName];}
function findChangedParamInSrvData(srvChagedParams,keystr){if(srvChagedParams[keystr]!=undefined){return true;}
return false;}
function enableParamControls(keystr){enableParamEditing(keystr)
return true;}
function updateParametersTranslation(){if(isDeviceGm3Conf()){return;}
$(".tdParamsDescr .paramsDescr").each(function(){if($(this).closest('div[id^="rmUserParams"]').length==0&&$(this).attr("bit")!="true"){$(this).empty();var paramName=$(this).attr("id").substring(11);$(this).append(translateParameter(paramName));}});setParameters(parameters_current,updater.editableParamsVer_,EDIT_PARAMS);}
function updateHeadersTranslation(){if(isDeviceGm3Conf()){return;}
fillParSectionTileDic(controller.protocol_type);$(".sectionHeader").each(function(){if($(this).closest('div[id^="rmUserParams"]').length==0){if($(this).find('span[id^="sectionHeaderText"]').length!=0){var text_el=$($(this).find('span[id^="sectionHeaderText"]')[0])
text_el.empty();var num=text_el.attr("id").substring(18);text_el.append(PAR_SECTION_TITLE[num]);}}});}
var is_econet=false;var panelVer=null;var clientId=null;var sectionETtranslations=null;var editParamsETtranslations=null;var choiceParamsETtranslations=null;var infoLangETtranslations=null;var alarmsETtranslations=null;var paramsETtranslations=null;var informationParamsValsETtranslations=null;var tilesParamsValsETtranslations=null;var ETunits=null;var ETsections=null;var ETeditableParams=null;var ETinformationParams=null;var ETchoiceParams=null;var ETparametersData=null;var ETbuttons=null;var ETserviceMenus=null;var ETlangNum=0;var ETtilesNames=null;var EThistoryParamsNames=null;var ETconfigEditableParams=null;var ETonOffGraph=null;PARAMS_WITH_AUTO={"WS3":0,"WS2":2};var showLoading=false;CLIENT_LANGUAGES={61:["en"],85:["pl"]}
var lastETpasswordVal=null;function showParamLoading(){if(!showLoading){showLoading=true;$("#confErrorDiv").hide();showDots();$("#rmLoader").show();}}
function clearETdata(){panelVer=null;clientId=null;sectionETtranslations=null;editParamsETtranslations=null;infoLangETtranslations=null;choiceParamsETtranslations=null;alarmsETtranslations=null;paramsETtranslations=null;ETunits=null;ETsections=null;ETeditableParams=null;ETinformationParams=null;ETchoiceParams=null;ETparametersData=null;ETbuttons=null;ETserviceMenus=null;ETlangNum=0;ETtilesNames=null;EThistoryParamsNames=null;etNewConfTrans=false;etConfVer='';ETconfigEditableParams=null;ETonOffGraph=null;}
function showDots(){if(showLoading){var d=$("#loadingDots");d.text().length>=3?d.text(''):d.append('.');setTimeout(showDots,300);}}
function stopShowLoading(){showLoading=false;$("#rmLoader").hide();}
function confDownloadSuccess(){stopShowLoading();$("#confErrorDiv").hide();}
function confDownloadError(error){stopShowLoading();$("#confErrorDiv").show();}
USER_PARAMS_SECTION=255
max_level=1;function setNewParametersStructureET(data,sections,editable,information,choice,buttons,serviceMenus,configEditableParams,configEditableParamsMulti,onOffGraph){ETparametersData=data;if(sections!=null&&(dictChanged(sections,ETsections)||dictChanged(editable,ETeditableParams)||infoChanged(information,ETinformationParams)||dictChanged(choice,ETchoiceParams)||dictChanged(ETbuttons,buttons)||dictChanged(configEditableParams,ETconfigEditableParams)||dictChanged(configEditableParamsMulti,ETconfigEditableParamsMulti)||dictChanged(onOffGraph,ETonOffGraph)||dictChanged(ETserviceMenus,serviceMenus)||$('#userParams').children().length==0)){ETsections=sections;ETeditableParams=editable;ETinformationParams=information;ETchoiceParams=choice;ETbuttons=buttons;ETserviceMenus=serviceMenus;ETconfigEditableParams=configEditableParams;ETconfigEditableParamsMulti=configEditableParamsMulti;ETonOffGraph=onOffGraph;if(ETonOffGraph){ETonOffGraph=prepareOnOffGraph(data);}
createParamsMenu();}else{updateParametersValues();showhideParameters();}
if(!tilesETFlag){createTilesGm(tiles_tab);}
if(!schemaVentFlag){if(!ngp_hide("diag")){schemaUpdateViewET(schema.img_id,schema.controllerID);}
schemaVentFlag=true;}}
function prepareOnOffGraph(data){var j=ETonOffGraph.length;var ETonOffGraphTMP=new Array();for(var i=0;i<j;i++){var row=ETonOffGraph[i];if(data[row[0]])
{var dataRow=data[row[0]];row[0]=dataRow["name"];ETonOffGraphTMP[row[0]]=row;}}
return ETonOffGraphTMP;}
function createParamsMenu(){buildMenuET();rebuildEditableParameters=true;showhideParameters();}
function dictChanged(newDict,oldDict){return!(JSON.stringify(newDict)===JSON.stringify(oldDict));}
function infoChanged(newList,oldList){if(newList.length!=oldList.length){return true;}else{if(!compareKeys(newList,oldList))
return true;var new_keys=Object.keys(newList);for(var i in new_keys){if(newList[new_keys[i]][0]!=oldList[new_keys[i]][0])
return true;}}
return false}
function compareKeys(a,b){var aKeys=Object.keys(a).sort();var bKeys=Object.keys(b).sort();return JSON.stringify(aKeys)===JSON.stringify(bKeys);}
function buildMenuET(){$('#userParams').children().remove();if(ngp_hide("menu_user")){return;}
$("div[id^='serviceParamsET']").each(function(){$(this).children().remove();});if(ETbuttons!=null){for(var i in ETbuttons){if(ETbuttons[i][2]){var type=ETbuttons[i][0];var num=ETbuttons[i][1];if(type==0){addEditableParamET(num,$('#userParams'),i);}else if(type==1){addChoiceParamET(num,$('#userParams'),i);}else if(type==7){addSectionET(num,$('#userParams'),0,i);}else if(type==8){addSectionET(parseInt(num)+99000+1,$('#userParams'),0,i);}}}
$("div[id^='serviceParamsET']").remove()
for(var i in ETserviceMenus){addServiceMenuET(ETserviceMenus[i],i);}
addCollapsiblePanels();var l=1;while($('.level'+l).length){if($('.level'+l).css("background-position-x")=="10px"){document.styleSheets[0].addRule('.level'+l,"margin-left: "
+(32+10*l)+"px;",1);}
l=l+1;}
showhideParameters();if($("#tabHrServiceParams").hasClass("current")){lastETpasswordCheck();}}}
function addEditableParamET(num,parent,buttonNum){if(num in ETeditableParams&&ETeditableParams[num][2]){var paramNum=ETeditableParams[num][0];if(ETparametersData[paramNum]!=undefined&&ETparametersData[paramNum]!=null){var unit=ETeditableParams[num][1];var listunit=getParamUnitStr(unit);var onclickFuncStr='"popupParamETeditable('+num+');"';var id=(buttonNum!=null?"button"+buttonNum:"editableParam"+num);var name=getETparamTranslation(id);var value=ETparametersData[paramNum].value;for(var i in ETconfigEditableParamsMulti){if(paramNum==ETconfigEditableParamsMulti[i][0]){value=ETconfigEditableParamsMulti[i][1]*value;value=value.toFixed(5);value=parseFloat(value);}}
var value_code='<span class="innerParamValue">'+value+'</span>'
var unit_code='<span class="innerParamUnit">'+listunit+'</span>'
var paramStr='<div class="paramsContainer" type="0" num="'
+num
+'"><table  class="etTableParamsSection">'
+'<tr class="two '
+ETparametersData[paramNum].name
+(ETparametersData[paramNum].edit?' click" onclick='
+onclickFuncStr:' disabled"')+'>'
+'<td class="tdParamsLeftMargin" ></td>'
+'<td class="tdParamsDescr" >'+'<div id="'+id
+'" class="paramsDescr'
+(buttonNum!=null?' button':'')+'">'+name
+'</div></td>'+'<td class="tdParamsValue" >'
+value_code+unit_code+'</td>'
+'<td class="tdParamsEdtype '
+(ETparametersData[paramNum].edit?'paramEditIco':'paramViewIco')
+'"><i class="paramRowIcon"></td>'+'</tr>'+'</table></div>';parent.append(paramStr);}}}
function addInformationParamET(num,parent){if(ETinformationParams!=undefined&&num in ETinformationParams&&ETinformationParams[num].length>1&&ETinformationParams[num][1]!=null&&ETinformationParams[num][0]!=null){var paramValues=ETinformationParams[num][1];if(paramValues.length>0){var paramValue=ETinformationParams[num][1][ETlangNum];if(paramValue==undefined||paramValue.length<2){paramValue=ETinformationParams[num][1][0];}
if(paramValue.length>2){var unit=paramValue[1];var listunit=getParamUnitStr(unit);var id="informationParam"+num;var name=getETparamTranslation(id);var value=paramValue[0];if(paramValue[2]==1){value=getETinformationParamTranslation(id,value)}
if(ETinformationParams[num][0]!=false){var value_code='<span class="innerParamValue">'+value+'</span>'
var unit_code='<span class="innerParamUnit">'+listunit+'</span>'}
else if(ETinformationParams[num][0]==false){var value_code='<span class="innerParamValue">'+"---"+'</span>'
var unit_code='<span class="innerParamUnit">'+'</span>'}
var paramStr='<div class="paramsContainer" type="99" num="'
+num+'"><table  class="etTableParamsSection">'
+'<tr class="two reado">'
+'<td class="tdParamsLeftMargin" ></td>'
+'<td class="tdParamsDescr" >'+'<div id="'+id
+'" class="paramsDescr">'+name+'</div></td>'
+'<td class="tdParamsValue" >'
+value_code+unit_code
+'</td>'+'<td class="tdParamsEdtype paramViewIco"><i class="paramRowIcon"></td></tr></table></div>';parent.append(paramStr);}}}}
function addChoiceParamET(num,parent,buttonNum){if(num in ETchoiceParams&&ETchoiceParams[num][2]){var onclickFuncStr='"popupParamETbit('+num+');"';var paramNum=ETchoiceParams[num][0];if(ETparametersData[paramNum]!=undefined&&ETparametersData[paramNum]!=null){var value=getParamBitValue(ETparametersData[paramNum].value,ETchoiceParams[num][1]);var id=(buttonNum!=null?"button"+buttonNum:"choiceParam"
+num);var name=getETparamTranslation(id);var value_code='<span class="innerParamValue" val="'+value+'">'+translateBitValue("choiceParam"+num,value)+'</span>'
var paramStr='<div class="paramsContainer" type="1" num="'+num
+'"><table  class="etTableParamsSection">'
+'<tr class="two '+ETparametersData[paramNum].name
+' click" onclick='+onclickFuncStr+'>'
+'<td class="tdParamsLeftMargin" ></td>'
+'<td class="tdParamsDescr" >'+'<div id="'+id
+'" class="paramsDescr'
+(buttonNum!=null?' button':'')+'" bit="true">'
+name+'</div></td>'+'<td class="tdParamsValue" >'
+value_code
+'</td>'+'<td class="tdParamsEdtype '
+(ETparametersData[paramNum].edit?'paramEditIco':'paramViewIco')
+'"><i class="paramRowIcon"></td></tr></table></div>';parent.append(paramStr);}}}
function addSectionET(num,parent,level,buttonNum){if(num in ETsections&&ETsections[num][1]){var name=(buttonNum!=null?getETparamTranslation("button"
+buttonNum):getETsectionTranslation(num));var sectionStr='<div id="sectionHeader_'+num
+'" style="margin-left: '+level*30+'px;" class="sectionHeader etSectionHeader'
+(buttonNum!=null?' button':'')+'" level = "'+level
+'" '
+(buttonNum!=null?' buttonNum = "'+buttonNum+'"':'')
+'><i class="paramArrIco" onclick="parentAction(\'sectionHeader_'+num+'\');"></i><span onclick="parentAction(\'sectionHeader_'+num+'\');" id="sectionHeaderText_'+num+'">'+name+'</span></div>'+'<div id="table_'+num
+'" style="margin-left: '+level*30+'px;" level = "'+level+'" class="etParamsSectionGroup"></div>';parent.append(sectionStr);var items=ETsections[num][2];for(var i=0;i<items.length;i+=1){var type=items[i][0];var itemNum=items[i][1];if(type==0){addEditableParamET(itemNum,$('#table_'+num));}else if(type==1){addChoiceParamET(itemNum,$('#table_'+num));}else if(type==7||type==8){addSectionET(itemNum,$('#table_'+num),level+1);}else if(type=="RO"){addInformationParamET(itemNum,$('#table_'+num));}}}}
function addServiceMenuET(num,menuNum){if(num in ETsections&&ETsections[num][1]){$('<div id="serviceParamsET'+menuNum+'"></div>').insertAfter('#serviceParams');$('#serviceParamsET'+menuNum).append('<div id="table_'+num
+'" class="level-1" level="-1"></div>');var items=ETsections[num][2];for(var i=0;i<items.length;i+=1){var type=items[i][0];var itemNum=items[i][1];if(type==0){addEditableParamET(itemNum,$('#table_'+num));}else if(type==1){addChoiceParamET(itemNum,$('#table_'+num));}else if(type==7){addSectionET(itemNum,$('#table_'+num),0);}}
$('#serviceParamsET'+menuNum).hide();}}
function updateParametersValues(){$(".paramsContainer").each(function(){var type=$(this).attr("type");var num=$(this).attr("num");if(type==0){var paramNum=ETeditableParams[num][0];var value=ETparametersData[paramNum].value;$(this).find('.innerParamValue').text(value);}else if(type==1){var paramNum=ETchoiceParams[num][0];var value=getParamBitValue(ETparametersData[paramNum].value,ETchoiceParams[num][1]);$(this).find('.innerParamValue').text(translateBitValue("choiceParam"+num,value));}else if(type==99){if(ETinformationParams!=undefined&&num in ETinformationParams&&ETinformationParams[num].length>1&&ETinformationParams[num][0]&&ETinformationParams[num][1]!=null){var paramValues=ETinformationParams[num][1];if(ETinformationParams[num][1].length>0){var paramValue=ETinformationParams[num][1][ETlangNum];if(paramValue==undefined||paramValue.length<2){paramValue=ETinformationParams[num][1][0];}
var id="informationParam"+num;var value=paramValue[0];if(paramValue[2]==1){value=getETinformationParamTranslation(id,value)}
if(paramValue.length>2){var unit=paramValue[1];var listunit=getParamUnitStr(unit);$(this).find('.innerParamValue').text(value);$(this).find('.innerParamUnit').text(listunit);}}}}});}
function updateHeadersTranslationET(){$(".sectionHeader").each(function(){if($(this).closest('div[id^="rmUserParams"]').length==0){if($(this).find('span[id^="sectionHeaderText"]').length!=0){var text_el=$($(this).find('span[id^="sectionHeaderText"]')[0])
text_el.empty();var num=text_el.attr("id").substring(18);var sectionName=($(this).hasClass("button")?getETparamTranslation("button"
+$(this).attr("buttonNum")):getEtTranslationByLangNum(sectionETtranslations[num]));if(sectionName==undefined){$(this).hide();}else{text_el.append(sectionName);$(this).show();}}}});}
function updateParametersTransaltionsET(){if(editParamsETtranslations==null){return;}
$(".tdParamsDescr .paramsDescr").each(function(){if($(this).closest('div[id^="rmUserParams"]').length==0){$(this).empty();var paramName=$(this).attr("id");$(this).append(getETparamTranslation(paramName));if($(this).attr("bit")=="true"){var valContainer=$(this).find(".innerParamValue");valContainer.empty();var val=parseInt(valContainer.attr("val"));var choiceParamNum=paramName.substring(11)
valContainer.append(translateBitValue(val,ETchoiceParams[choiceParamNum]));}}});}
function getParamBitValue(value,settings){for(var v in settings){if(settings[v][0]==0){if(value==0){return v;}}else{var setBits=value&settings[v][0];var clearedBits=value&settings[v][1];if((setBits==settings[v][0]&&clearedBits==0)){return v;}}}
if(value==0){return 0;}
return NAN_REPR;}
function translateBitValue(paramName,val){if(choiceParamsETtranslations!=null&&choiceParamsETtranslations[paramName]!=null&&val!="---"){var paramdata=choiceParamsETtranslations[paramName]
return getEtTranslationByLangNum(paramdata[parseInt(val)]);}
return val;}
function getETparamTranslation(paramNum){if(editParamsETtranslations!=null&&editParamsETtranslations[paramNum]!=null){return getEtTranslationByLangNum(editParamsETtranslations[paramNum]);}else{return null;}}
function getETinformationParamTranslation(paramKey,value){if(informationParamsValsETtranslations!=null&&informationParamsValsETtranslations[paramKey]!=null){return getEtTranslationByLangNum(informationParamsValsETtranslations[paramKey][parseInt(value)]);}else{return translate(value);}}
function getETtilesParamTranslation(paramIndex,value){if(tilesParamsValsETtranslations!=null&&tilesParamsValsETtranslations[paramIndex]!=null){return getEtTranslationByLangNum(tilesParamsValsETtranslations[paramIndex][parseInt(value)]);}else{return translate(value);}}
function getETsectionTranslation(secNum){if(sectionETtranslations!=null){return getEtTranslationByLangNum(sectionETtranslations[secNum]);}else{return null;}}
function downloadETtranslations(){if(clientId in CLIENT_LANGUAGES||etNewConfTrans){if(!etTranslationsExisit()){controller.getETtranslations(panelVer,clientId,"",getETtranslationsResponse,getETtranslationsError);}else{translateET();}}else{controller.getETtranslations(panelVer,clientId,currLang,getETtranslationsResponse,getETtranslationsError);}}
function getEtTranslationByLangNum(text){var textout=text;if(ETlangNum!=null&&text!=undefined&&typeof(text)!="string"){if(ETlangNum>-1&&ETlangNum<text.length){return removeComputedChars((text[ETlangNum]!="_"?text[ETlangNum]:text[0]));}
return removeComputedChars(text[0]);}
return removeComputedChars(textout);}
function removeComputedChars(intext){if(typeof(intext)=="string"){var paramStart=intext.indexOf('|');var paramEnd=intext.indexOf('||');if(paramEnd>paramStart){var pardata=intext.slice(paramStart+1,paramEnd);intext=intext.replace("|"+pardata+"||","");}}
return intext}
function getLangNumberValue(select_key){if(select_key===undefined){select_key=currLang;}
ETlangNum=-1;var english_id=0;if(infoLangETtranslations!=null&&infoLangETtranslations[0]!=undefined&&infoLangETtranslations[0]!=null){const lang_codes=infoLangETtranslations[0];for(const ii in lang_codes){if(lang_codes[ii]==select_key){ETlangNum=ii;return;}
if(lang_codes[ii]=="en"){english_id=ii;}}}
if(ETlangNum==-1){ETlangNum=english_id;}}
function getETtranslationsResponse(result,textStatus,xmlhttprequest){if(result!=null&&result!=""){sectionETtranslations=result.sections;editParamsETtranslations=result.editParams;choiceParamsETtranslations=result.choiceParams;alarmsETtranslations=result.alarms;paramsETtranslations=result.long_names;ETtilesNames=result.tiles;EThistoryParamsNames=result.history;ETunits=result.units
if(result.transInfo!=undefined){infoLangETtranslations=result.transInfo;getLangNumberValue();}
if(result.infoParams!=undefined){informationParamsValsETtranslations=result.infoParams}
if(result.tilesParams!=undefined){tilesParamsValsETtranslations=result.tilesParams}
if(etTranslationsExisit){$("#translationsErrorDiv").hide();}
translateET();createParamsMenu();if(!$.isEmptyObject(tiles_params)){createTilesET();}}else{retryDownloadETtranslations();}}
function translateET(){updateHeadersTranslationET();updateParametersTransaltionsET();showhideParameters();alarmsResponseRefresh();translateTilesHeaders();updateStaticGm();if(EThistoryParamsNames!=null){if(typeof updateDataHistorySelectTranslationET=='function'){updateDataHistorySelectTranslationET();}}else if(typeof updateDataHistorySelectTranslation=='function'){updateDataHistorySelectTranslation();}
translateETschema();updateParametersValues();}
function getETtranslationsError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);retryDownloadETtranslations();}
function retryDownloadETtranslations(){if(controller.protocol_type!=""){setTimeout(downloadETtranslations,10000);$("#translationsErrorDiv").show();showhideParameters();}}
function etTranslationsExisit(){return sectionETtranslations!=null&&editParamsETtranslations!=null&&choiceParamsETtranslations!=null}
function isServiceMenuExists(){var res=false
$("div[id^='serviceParamsET']").each(function(){if($(this).children().length!=0){res=true;}});return res}
function showhideParameters(){if(ngp_hide("menu_service")||!isServiceMenuExists()||!etTranslationsExisit()){removeTabFromMenu("tabHrServiceParams");}else{addTabToMenu("tabHrServiceParams");}
if(ngp_hide("menu_user")||$('#userParams').children().length==0||!etTranslationsExisit()){$('#userParams').hide();$('#userParamsErr').show();removeTabFromMenu("tabHrUserParams");}else{$('#userParams').show();$('#userParamsErr').hide();addTabToMenu("tabHrUserParams");}}
function setPanelVer(ver,client,controllerID){if(panelVer!=ver||clientId!=client||schema.controllerID!=controllerID){panelVer=ver;clientId=client;schema.controllerID=controllerID;downloadETtranslations();if(panelVer!=null&&panelVer.length!=0){var versions=panelVer.split("_");$("#lbPanelConfVerCurr").text(versions[1]);$("#trPanelConfVer").show();}else{$("#lbPanelConfVerCurr").text("");$("#trPanelConfVer").hide();}}}
function getETtileTranslation(param){if(ETtilesNames!=null&&parseInt(param)+1 in ETtilesNames){return ETtilesNames[parseInt(param)+1];}
if(paramsETtranslations!=null&&param in paramsETtranslations){return paramsETtranslations[param];}
return param;}
PARAM_TEXT_CONVERSIONS={0:floatToString,1:onOffConversion,4:roundedValToString,6:onOffConversionWithText,7:valToStringMult,8:valToText,9:bitsToText,}
function floatToString(settings,val){var precision=1;if(settings.length>4){precision=parseInt(settings[4])-100;}
return val.toFixed(precision);}
function onOffConversion(settings,val){var settedBits=parseInt(settings[4]);if(settedBits&val==settedBits)
return"on";return"off";}
function roundedValToString(settings,val){return val.toFixed();}
function valToText(settings,val){var num=parseInt(settings[4])
for(var i=0;i<num;i+=1){if(val==settings[5+i]){return settings[5+num+i];}}
return"";}
function bitsToText(settings,val){var num=parseInt(settings[4])
for(var i=0;i<num;i+=1){var bits=parseInt(settings[5+i]);if(val&bits==bits){return settings[5+num+i];}}
return"";}
function onOffConversionWithText(settings){var val=getCurrParamByNumber(settings[1]);if(val!=null){var settedBits=parseInt(settings[4]);if(settedBits&val==settedBits)
return settings[5];return settings[6];}
return"---";}
function valToStringMult(settings){var val=getCurrParamByNumber(settings[1]);if(val!=null){return val*parseInt(settings[4]);}
return"---";}
function findEditableParamNum(paramNum){for(var key in ETeditableParams){var param=ETeditableParams[key];if(param!=null&&param[0]==paramNum){return key}}
return null;}
function checkETpassword(){controller.getETPassword(checkETPasswordResponse);}
function lastETpasswordCheck(){if(lastETpasswordVal!=null){controller.getETPassword(checkLastETPasswordResponse);}}
function checkLastETPasswordResponse(result,textStatus,xmlhttprequest){showHideEtMenu(lastETpasswordVal,result)}
function checkETPasswordResponse(result,textStatus,xmlhttprequest){var passwd=$('#inpServicePasswd').val();if(showHideEtMenu(getSHA512(passwd),result)){closeEditWindow('#secAskServicePassword');}else{$('#askPasswordWindowInfoArea').text(translate('wrong_password'));$('#askPasswordWindowInfoArea').show();}}
function showHideEtMenu(passwd,result){lastETpasswordVal=passwd;for(var i in result){if(result[i]==passwd){if($('#serviceParamsET'+i+' .paramsContainer').length>0){showTab('ServiceParams','ServiceParams');$('#serviceParamsET'+i).siblings().hide();$('#serviceParamsET'+i).show();}
else{$('#serviceParamsErr').siblings().hide();$('#serviceParamsErr').show();}
return true;}}
return false;}
function showETPasswordPrompt(){if(!checkCurrentDevActive())
return;$('#askPasswordWindowTitle').text(translate('password'));$('#popupPasswdOK').text(translate('ok'));$('#popupPasswdCancel').text(translate('cancel'));$('#popupPasswdDesc').text(translate('enter_password'));preparePasswordPopup("checkETpassword();","return closeEditWindow('#secAskServicePassword');","return validatePassword(event, checkETpassword);",{})
showEditWindow('#secAskServicePassword');$('#inpServicePasswd').trigger("focus");}
var remote_menu_structure=null;var remote_menu_paramsnames=null;var remote_menu_catsnames=null;var remote_menu_paramsunitsnames=null;var remote_menu_paramsenums=null;var remote_menu_locksnames=null;var remote_menu_paramsdata=null;var remote_menu_currdatadisp=null;var remote_menu_paramsdescs=null;var remote_menu_catsdescs=null;var reg_current_parameters=null;var RM_STRUCTURE=1;var RM_PARAMSNAMES=2;var RM_CATSNAMES=3;var RM_CURRDATADISP=4;var RM_PARAMSDATA=5;var RM_PARAMSUNITSNAMES=6;var RM_PARAMSENUMS=7;var RM_LOCKSNAMES=8;var RM_PARAMSDESCS=9;var RM_CATSDESCS=10;var shared_sections=new Object()
function setParametersRM(params,version,type){if(params!=null){var recreate=false;switch(type){case RM_PARAMSNAMES:case RM_CATSNAMES:case RM_PARAMSUNITSNAMES:case RM_PARAMSENUMS:case RM_LOCKSNAMES:case RM_STRUCTURE:case RM_CURRDATADISP:case RM_PARAMSDATA:case RM_PARAMSDESCS:case RM_CATSDESCS:if(type==RM_PARAMSNAMES){if(remote_menu_paramsnames==null){remote_menu_paramsnames=params}else{if(!areEqualLengths(remote_menu_paramsnames,params)){recreate=true}
remote_menu_paramsnames=params}
updater.remoteMenuVer_[REMOTE_MENU_PARAMS_NAMES_]=version;}
if(type==RM_CATSNAMES){if(remote_menu_catsnames==null){remote_menu_catsnames=params}else{if(!areEqualLengths(remote_menu_catsnames,params)){recreate=true}
remote_menu_catsnames=params}
updater.remoteMenuVer_[REMOTE_MENU_CATS_NAMES_]=version;}
if(type==RM_PARAMSUNITSNAMES){if(remote_menu_paramsunitsnames==null){remote_menu_paramsunitsnames=params}else{if(!areEqualLengths(remote_menu_paramsunitsnames,params)){recreate=true}
remote_menu_paramsunitsnames=params}
updater.remoteMenuVer_[REMOTE_MENU_PARAMS_UNITS_NAMES_]=version;}
if(type==RM_PARAMSDESCS){if(remote_menu_paramsdescs==null){remote_menu_paramsdescs=params}else{if(!areEqualLengths(remote_menu_paramsdescs,params)){recreate=true}
remote_menu_paramsdescs=params}
updater.remoteMenuVer_[REMOTE_MENU_PARAMS_DESCS_]=version;}
if(type==RM_CATSDESCS){if(remote_menu_catsdescs==null){remote_menu_catsdescs=params}else{if(!areEqualLengths(remote_menu_catsdescs,params)){recreate=true}
remote_menu_catsdescs=params}
updater.remoteMenuVer_[REMOTE_MENU_CATS_DESCS_]=version;}
if(type==RM_LOCKSNAMES){if(remote_menu_locksnames==null){remote_menu_locksnames=params}else{if(!areEqualLengths(remote_menu_locksnames,params)){recreate=true}
remote_menu_locksnames=params}
updater.remoteMenuVer_[REMOTE_MENU_LOCKS_NAMES_]=version;}
if(type==RM_PARAMSENUMS){if(remote_menu_paramsenums==null){remote_menu_paramsenums=params}else{if(!areEqualLengths(remote_menu_paramsenums,params)){recreate=true}
remote_menu_paramsenums=params}
updater.remoteMenuVer_[REMOTE_MENU_ENUMS_NAMES_]=version;}
if(type==RM_STRUCTURE){remote_menu_structure=params
recreate=true
updater.remoteMenuVer_[REMOTE_MENU_STRUCTURE_]=version;}
if(type==RM_PARAMSDATA){if(remote_menu_paramsdata==null){remote_menu_paramsdata=params}else{if(!areEqualLengths(remote_menu_paramsdata,params)){recreate=true}
remote_menu_paramsdata=params}
if(version.length>1){updater.remoteMenuVer_[REMOTE_MENU_PARAMS_KONF_]=version[0];updater.remoteMenuVer_[REMOTE_MENU_PARAMS_VALUES_]=version[1];}else{updater.remoteMenuVer_[REMOTE_MENU_PARAMS_VALUES_]=version;}}
if(remote_menu_structure!=null&&remote_menu_paramsnames!=null&&remote_menu_catsnames!=null&&remote_menu_paramsdata!=null&&remote_menu_paramsunitsnames!=null&&remote_menu_paramsenums!=null&&remote_menu_locksnames!=null&&remote_menu_paramsdescs!=null&&remote_menu_catsdescs!=null){if($('#rmUserParams').children().length==0||recreate){updateRemoteMenuParametersView()}else{if(type==RM_PARAMSDATA||type==RM_PARAMSNAMES||type==RM_PARAMSUNITSNAMES||type==RM_PARAMSENUMS||type==RM_PARAMSDESCS){updateRemoteMenuParametersOnly();}else if(type==RM_CATSNAMES||type==RM_CATSDESCS){updateRemoteMenuSectionsOnly();}}}
break;}}else{switch(type){case RM_PARAMSNAMES:remote_menu_paramsnames=null;case RM_CATSNAMES:remote_menu_catsnames=null;case RM_PARAMSUNITSNAMES:remote_menu_paramsunitsnames=null;case RM_LOCKSNAMES:remote_menu_locksnames=null;case RM_PARAMSENUMS:remote_menu_paramsenums=null;case RM_PARAMSDESCS:remote_menu_paramsdescs=null;case RM_CATSDESCS:remote_menu_catsdescs=null;case RM_STRUCTURE:remote_menu_structure=null;case RM_PARAMSDATA:remote_menu_paramsdata=null;default:if(remote_menu_structure==null||remote_menu_paramsnames==null||remote_menu_catsnames==null||remote_menu_paramsdata==null||remote_menu_paramsunitsnames==null||remote_menu_paramsenums==null||remote_menu_locksnames==null){cleanRMParameters()}
break;}}}
function findChangedParamRMInSrvData(srvChagedParams,keystr,type){for(var obj in srvChagedParams){var paramObj=srvChagedParams[obj]
if(paramObj.name!=undefined&&paramObj.type!=undefined&&paramObj.name==keystr&&paramObj.type==type){return true;}}
return false}
function enableParamRMControls(keystr){var tilesReload=false;if(changedParams[keystr].type==RM_PARAM_NAME_TYPE){enableRMParamEditing(keystr);}else if(changedParams[keystr].type==RM_KEYPARAM_NAME_TYPE){enableRMTileParamEditing(keystr);tilesReload=true;}
delete changedParams[keystr]
return tilesReload;}
function getRegParamsDataResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null){reg_current_parameters=result.data
updateRemoteMenuParametersOnly()
if(!$.isEmptyObject(changedParams)){var keys=Object.keys(changedParams);var tilesReload=false;if(result.changedParams!=undefined&&!$.isEmptyObject(result.changedParams)){for(var key in keys){var keystr=keys[key]
if(!findChangedParamRMInSrvData(result.changedParams,keystr,changedParams[keystr].type)){if((changedParams[keystr].type==RM_PARAM_NAME_TYPE||changedParams[keystr].type==RM_KEYPARAM_NAME_TYPE)&&parseInt(keystr)in disabledList&&remote_menu_paramsdata[keystr].value==disabledList[parseInt(keystr)]){tilesReload=enableParamRMControls(keystr);delete disabledList[parseInt(keystr)];}}}}else{for(var key in keys){var keystr=keys[key];if((changedParams[keystr].type==RM_PARAM_NAME_TYPE||changedParams[keystr].type==RM_KEYPARAM_NAME_TYPE)&&parseInt(keystr)in disabledList&&remote_menu_paramsdata[keystr].value==disabledList[parseInt(keystr)]){tilesReload=enableParamRMControls(keystr);delete disabledList[parseInt(keystr)];}}}
if(tilesReload){updateStatic();}}}}
function updateRemoteMenuView(){if($('#rmUserParams').children().length==0){if(remote_menu_structure!=null&&remote_menu_paramsnames!=null&&remote_menu_catsnames!=null&&remote_menu_paramsdata!=null&&remote_menu_paramsunitsnames!=null&&remote_menu_paramsenums!=null){updateRemoteMenuParametersView()}}}
function getRemoteMenuParamsNamesResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuParamsNamesVer!=undefined)?result.remoteMenuParamsNamesVer:result.version,RM_PARAMSNAMES);}else{setParameters(null);}}
function getRemoteMenuCatsNamesResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuCatsNamesVer!=undefined)?result.remoteMenuCatsNamesVer:result.version,RM_CATSNAMES);}else{setParameters(null);}}
function getRemoteMenuParamsUnitsNamesResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuParamsUnitsNamesVer!=undefined)?result.remoteMenuParamsUnitsNamesVer:result.version,RM_PARAMSUNITSNAMES);}else{setParameters(null);}}
function getRemoteMenuParamsEnumsResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuParamsEnumsVer!=undefined)?result.remoteMenuParamsEnumsVer:result.version,RM_PARAMSENUMS);}else{setParameters(null);}}
function getRemoteMenuParamsDescsResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuParamsDescsVer!=undefined)?result.remoteMenuParamsDescsVer:result.version,RM_PARAMSDESCS);}else{setParameters(null);}}
function getRemoteMenuCatsDescsResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuCatsDescsVer!=undefined)?result.remoteMenuCatsDescsVer:result.version,RM_CATSDESCS);}else{setParameters(null);}}
function getRemoteMenuLocksNamesResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,(result.remoteMenuLocksNamesVer!=undefined)?result.remoteMenuLocksNamesVer:result.version,RM_LOCKSNAMES);}else{setParameters(null);}}
function getRemoteMenuStructureResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){setParameters(result.data,result.remoteMenuStructureVer,RM_STRUCTURE);}else{setParameters(null);}}
function getRemoteMenuCurrDataDispResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&Object.keys(result.data).length>0){remote_menu_currdatadisp=result.data
updater.remoteMenuVer_[REMOTE_MENU_CURRDATA_DISP_]=(result.remoteMenuCurrDataParamsVer!=undefined)?result.remoteMenuCurrDataParamsVer:result.version;}}
function getRemoteMenuParamsDataResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){if(result.remoteMenuValuesParamsVer!=undefined){setParameters(result.data,result.remoteMenuValuesParamsVer,RM_PARAMSDATA);}else{setParameters(result.data,[result.remoteMenuValuesKonfVer,result.remoteMenuValuesVer],RM_PARAMSDATA);}}else{setParameters(null);}}
function cleanRMParameters(){if(controller.type_==ECOMAX_850i_TYPE){var parentElement=$('#rmUserParams').parent();parentElement.append($('#rmUserParams'));}
$('#rmUserParams').children().remove();$("[id^='rmSectionHeader_']").remove();$("[id^='rmSectionTable_']").remove();}
function addRMCollapsiblePanels(){if($('#rmUserParams .rmSectionHeader').length>1){$("#rmUserParams [id^='rmTable_']").hide();}
if($('#rmUserParams .rmSectionHeader').length>1){$("#rmUserParams .rmSectionHeader").each(function(){var index=this.id.substr(16);var option=null;if(index.split('_').length>1){var options=index.split('_');index=options[0]
option=options[1]}
if(option!=null){if(option=='pass'){$(this).on("click",function(){if(rms_l<=0){showRMPasswordPrompt($(this).attr('id'))}else{$('#rmUserParams #rmTable_'+index).slideToggle('slow');if($(this).hasClass("extended")){$(this).removeClass("extended");rms_l=-1;}
else{$(this).addClass("extended");}}});}}else{$(this).on("click",function(){$('#rmUserParams #rmTable_'+index).slideToggle('slow');if($(this).hasClass("extended")){$(this).removeClass("extended");}
else{$(this).addClass("extended");}});}});}}
function updateRemoteMenuSectionsOnly(){parents_iterator=0;for(var i in remote_menu_structure){var element=remote_menu_structure[i];var type=element['type'];var element_index=element['index'];if(type==0||type==2||type==4||type==5){if(parents_iterator>0){$('#rmSectionHeaderText_'+parents_iterator).text(getRmCatName(element_index));$('#rmSectionHeader_'+parents_iterator).attr('title',getRmCatDescTitle(element_index,false));if($('#rmSectionHeader_'+parents_iterator+"_pass").length){$('#rmSectionHeaderText_'+parents_iterator+"_pass").text(getRmCatName(element_index));$('#rmSectionHeader_'+parents_iterator+"_pass").attr('title',getRmCatDescTitle(element_index,false));}}
parents_iterator++;}}}
function getParentIterator(parent_iterator){if(shared_sections!=null&&shared_sections[parent_iterator]!=undefined){parent_iterator=shared_sections[parent_iterator]}
return parent_iterator}
function updateRemoteMenuParametersOnly(){for(var i in remote_menu_structure){var element=remote_menu_structure[i];var type=element['type'];var element_index=element['index'];var data_id=null;if('data_id'in element){data_id=element['data_id'];}
if(type==1){$('#lbEditParam'+element_index).text(getRmParamName(element_index));$('#lbEditParamValue'+element_index).text(getRmParamValue(element_index));$('#lbEditParamUnit'+element_index).text(getRmParamValueUnit(element_index));var tr_element=$('#lbEditParamValue'+element_index).parent().parent()
tr_element.attr('title',getRmParamDescTitle(element_index,false));}
if(type==3){$('#lbEditParamCurr'+data_id).text(getRmCurrentParamName(data_id));$('#lbEditParamValueCurr'+data_id).text(getRmParamCurrentValue(data_id));$('#lbEditParamUnitCurr'+data_id).text(getRmCurrentParamValueUnit(data_id));}}}
function updateRemoteMenuParametersView(){cleanRMParameters();$('#userParamsErr').hide();$('#serviceParamsErr').hide();parents_iterator=0;child_counter_iterator=0;var tr_class='one'
var hide_elements=new Array();var last_section_title='';var last_section_parent_iterator=-1;var pass_view_password_parent=-1;var last_cat_type=0;for(var i in remote_menu_structure){var element=remote_menu_structure[i];var type=element['type'];var element_index=element['index'];var pass_index=element['pass_index'];var data_id=null;if('data_id'in element){data_id=element['data_id'];}
if(type==7){if(i>2){child_counter_iterator++;tr_class='one'}}
if(type==0||type==2||type==4||type==5){var pass_suff=''
if(type==5){pass_suff='_pass'}
if(type==0||type==2){last_cat_type=type}
if(pass_index!=0){if(pass_index!=rms_l){hide_elements.push(parents_iterator)}else{if(rms_r=="view"){pass_view_password_parent=parents_iterator;}}}
if(hide_elements.indexOf(child_counter_iterator)!=-1){hide_elements.push(parents_iterator)}else if(hide_elements.indexOf(parents_iterator)==-1){if(last_section_title==''||last_section_title!=getRmCatName(element_index)||last_cat_type!=2){var section_code='<div id="rmSectionHeader_'+parents_iterator+pass_suff+'" class="rmSectionHeader"'+getRmCatDescTitle(element_index,true)+' style="margin-left: "><i class="paramArrIco"></i><span id="rmSectionHeaderText_'+parents_iterator+pass_suff+'">'+getRmCatName(element_index)+'</span></div>'
+'<div id="rmTable_'+parents_iterator+'"></div>';if(parents_iterator>0){if(child_counter_iterator==0){var style='margin-left: 0px;';var style_table='padding-left: 0px;';section_code=section_code.replace('margin-left: ',style).replace('padding-left: ',style_table);$('#rmUserParams').append(section_code);}else{var sec_element=$('#rmSectionHeader_'+child_counter_iterator);if(!sec_element.length){sec_element=$('#rmSectionHeader_'+child_counter_iterator+"_pass");}
var new_padding_value=parseInt(sec_element.css("margin-left"))+30;var style='margin-left: '+new_padding_value+'px;';var style_table='padding-left: '+new_padding_value+'px;';section_code=section_code.replace('margin-left: ',style).replace('padding-left: ',style_table);$('#rmTable_'+child_counter_iterator).append(section_code);}}
last_section_title=getRmCatName(element_index)
last_section_parent_iterator=parents_iterator}else{shared_sections[parents_iterator]=last_section_parent_iterator}}
parents_iterator++;}
if(type==1||type==3){if(hide_elements.indexOf(child_counter_iterator)==-1){onclickFuncStr=undefined
if(type==1)
onclickFuncStr='"rmPopupParam(\''+i+'\',\''+element_index+'\');"';if(pass_view_password_parent>-1&&child_counter_iterator>=pass_view_password_parent){onclickFuncStr=undefined}
var value_code='<span id="lbEditParamValue'+(type==3?('Curr'+data_id):element_index)+'" class="innerParamValue" '+'>'+(type==3?getRmParamCurrentValue(data_id):getRmParamValue(element_index))+'</span>'
var unit_code='<span id="lbEditParamUnit'+(type==3?('Curr'+data_id):element_index)+'" class="innerParamUnit" '+'>'+(type==3?getRmCurrentParamValueUnit(data_id):getRmParamValueUnit(element_index))+'</span>'
var parameter_code='<tr class="'+tr_class+(onclickFuncStr!=undefined?' click" onclick='+onclickFuncStr:' reado"')+(type==1?getRmParamDescTitle(element_index,true):'')+'>'+
'<td class="tdParamsLeftMargin" >'+''+
'<div id="lbEdit"></div></td>'+
'<td class="tdParamsDescr" >'+'<div id="lbEditParam'+(type==3?('Curr'+data_id):element_index)+'" class="paramsDescr">'+(type==3?getRmCurrentParamName(data_id):getRmParamName(element_index))+'</div></td>'+
'<td class="tdParamsValue" >'+value_code+unit_code+'</td>'+
'<td class="tdParamsEdtype '+(onclickFuncStr!=undefined?'paramEditIco':'paramViewIco')+'" ><i class="paramRowIcon"></td>'+
'</tr>';if(tr_class=='one'){tr_class='two'}else{tr_class='one'}
var margin=$('#rmTable_'+child_counter_iterator).parentsUntil('#rmUserParams').length
if($('#rmSectionTable_'+child_counter_iterator+'_'+$('#rmTable_'+child_counter_iterator+' div[id*="rmSectionHeader"]').length).length==0)
$('#rmTable_'+child_counter_iterator).append('<table id="rmSectionTable_'+child_counter_iterator+'_'+$('#rmTable_'+child_counter_iterator+' div[id*="rmSectionHeader"]').length+'" class="rmTableParamsSection" style="padding-left: '+(margin*30)+'px;"></table>')
var last_element_id=$('#rmTable_'+child_counter_iterator).children().last().attr('id')
if(last_element_id!=undefined&&last_element_id.indexOf('rmTable')!=-1){$('#rmTable_'+child_counter_iterator).append('<table id="rmSectionTable_'+child_counter_iterator+'_'+$('#rmTable_'+child_counter_iterator+' div[id*="rmSectionHeader"]').length+'" class="rmTableParamsSection" style="padding-left: '+(margin*30)+'px;"></table>')}
if(child_counter_iterator==0){var code='<div id="rmMainTable_0_'+parents_iterator+'"><table id="rmSectionTable_0_'+parents_iterator+'" class="rmTableParamsSection" style="padding-left: 0px;">'+parameter_code+'</table></div>'
$('#rmUserParams').append(code);}else{var tableid='#rmSectionTable_'+getParentIterator(child_counter_iterator)+'_'+$('#rmTable_'+getParentIterator(child_counter_iterator)+' div[id*="rmSectionHeader"]').length
var tablec=$(tableid)
var nextclass='two'
var change_class=false;if($(tableid+' tbody tr:last').hasClass('two'))
change_class=true
nextclass='one'
tablec.append(parameter_code);if(change_class){$(tableid+' tbody tr:last').removeClass('two')
$(tableid+' tbody tr:last').addClass('one')}else{$(tableid+' tbody tr:last').removeClass('one')
$(tableid+' tbody tr:last').addClass('two')}}}}}
if($('#rmUserParams').children().length==0&&$('#userParams').children().length==0){$('#userParamsErr').show();}
if(!ngp_hide("menu_user")&&$('#rmUserParams').children().length!=0){addTabToMenu("tabHrUserParams");}
if($('#rmUserParams').children().length!=0){removeTabFromMenu("tabHrServiceParams");}
changedParams={}
addRMCollapsiblePanels();}
function getRmCatName(index){if(remote_menu_catsnames!=null&&index<remote_menu_catsnames.length)
return remote_menu_catsnames[index]
return'---'}
function getRmParamDescTitle(index,full){if(remote_menu_paramsdescs!=null&&index<remote_menu_paramsdescs.length)
if(full){return' title="'+remote_menu_paramsdescs[index]+'"';}else{return remote_menu_paramsdescs[index];}
return''}
function getRmCatDescTitle(index,full){if(remote_menu_catsdescs!=null&&index<remote_menu_catsdescs.length)
if(full){return' title="'+remote_menu_catsdescs[index]+'"';}else{return remote_menu_catsdescs[index];}
return''}
function getRmParamData(index){if(remote_menu_paramsdata!=null&&index<remote_menu_paramsdata.length)
return remote_menu_paramsdata[index]
return null}
function getRmParamName(index){if(remote_menu_paramsnames!=null&&index<remote_menu_paramsnames.length)
return remote_menu_paramsnames[index]
return'---'}
function getRmCurrentParamName(data_id){if(remote_menu_currdatadisp!=null&&data_id in remote_menu_currdatadisp){curr_data_element=remote_menu_currdatadisp[data_id]
if('name'in curr_data_element){return curr_data_element['name'];}}
return'---'}
function getRmLockName(index){if(remote_menu_locksnames!=null&&index<remote_menu_locksnames.length)
return remote_menu_locksnames[index]
return'---'}
function getRmParamOrgValue(index){var value='---'
if(remote_menu_paramsdata!=null&&index<remote_menu_paramsdata.length){var param_desc=remote_menu_paramsdata[index]
value=param_desc.value;}
return value}
function getRmParamValue(index){if(remote_menu_paramsdata!=null&&index<remote_menu_paramsdata.length){var param_desc=remote_menu_paramsdata[index]
var value=param_desc.value;var unit=param_desc.unit;var mult=param_desc.mult;var offset=param_desc.offset;if(value==null){value=NAN_REPR;}else if(unit==ENUM_UNIT){if(typeof value=='boolean')
value=value?1:0;value=getRmParamEnumValue(offset,value)}else{var precision=getNumberPrecision(mult);if(precision>0){value=value.toFixed(precision+3);value=value.substring(0,value.length-4+precision);}}
return value}
return'---'}
function getRmParamCurrentValue(data_id){if(reg_current_parameters!=null&&data_id in reg_current_parameters&&remote_menu_currdatadisp!=null&&data_id in remote_menu_currdatadisp){var curr_data_element=remote_menu_currdatadisp[data_id]
var value=reg_current_parameters[data_id]
var unit_id=curr_data_element['unit'];var special=curr_data_element['special'];if(value==null){value=NAN_REPR;}else{if(unit_id>=ENUM_UNIT){if(typeof value=='boolean')
value=value?1:0;if(value!=undefined&&value!=null){value=getRmParamEnumValue(special,value)}}else{if(value!=undefined&&value!=null&&!isNaN(value)&&typeof value!='string'){value=value.toFixed(special);}}}
return value}
return'---'}
function getRmUnitByIndex(index){if(remote_menu_paramsunitsnames!=null&&index<remote_menu_paramsunitsnames.length){return remote_menu_paramsunitsnames[index]}
return""}
function getRmParamValueUnit(index){if(remote_menu_paramsdata!=null&&index<remote_menu_paramsdata.length){var param_desc=remote_menu_paramsdata[index]
var unit=param_desc.unit;if(unit==ENUM_UNIT){return"";}
if(remote_menu_paramsunitsnames!=null&&unit<remote_menu_paramsunitsnames.length){return remote_menu_paramsunitsnames[unit]}}
return'---'}
function getRmCurrentParamValueUnit(data_id){if(remote_menu_currdatadisp!=null&&data_id in remote_menu_currdatadisp){curr_data_element=remote_menu_currdatadisp[data_id]
if('unit'in curr_data_element){unit_id=curr_data_element['unit'];if(unit_id==ENUM_UNIT){return"";}
if(unit_id<remote_menu_paramsunitsnames.length){return remote_menu_paramsunitsnames[unit_id]}}}
return'---'}
function getRmParamEnumValue(offset,value){if(remote_menu_paramsenums!=null&&offset<remote_menu_paramsenums.length){var enum_element=remote_menu_paramsenums[offset]
var enum_first=enum_element.first
var enum_index=value-enum_first
var enum_values=enum_element.values
if(enum_index<enum_values.length){return enum_values[enum_index]}}
return value}
function getRmCurrDisp(current_key){if(remote_menu_currdatadisp!=null&&current_key in remote_menu_currdatadisp)
return remote_menu_currdatadisp[current_key]
return null}
function getRmCurrEdit(current_key){if(current_params_edits!=null&&current_key in current_params_edits)
return current_params_edits[current_key]
return null}
function showRMPasswordPrompt(id){if(!checkCurrentDevActive())
return;$('#askPasswordWindowTitle').text(translate('password'));$('#popupPasswdOK').text(translate('ok'));$('#popupPasswdCancel').text(translate('cancel'));$('#popupPasswdDesc').text(translate('enter_password'));preparePasswordPopup("checkRMPassword();","return closeEditWindow('#secAskServicePassword');","return validatePassword(event, checkRMPassword);",{'source-section-id':id})
showEditWindow('#secAskServicePassword');$('#inpServicePasswd').trigger("focus");}
function checkRMPassword(){controller.rmCheckAccess(getSHA512($('#inpServicePasswd').val()),checkRMPasswordResult,checkRMPasswordError)}
function checkRMPasswordResult(result,textStatus,xmlhttprequest){if(!result.access){$('#askPasswordWindowInfoArea').text(translate('wrong_password'));$('#askPasswordWindowInfoArea').show();}else{closeEditWindow('#secAskServicePassword');$('#inpServicePasswd').val("");rms_l=result.index
rms_r=result.level
updateRemoteMenuParametersView();var section_id='#'+$('#askPasswordWindowContent').attr('source-section-id');var index=section_id.substr(17);if(index.split('_').length>1){var options=index.split('_')
index=options[0]}
$('#rmUserParams #rmTable_'+index).slideToggle('slow');if($(section_id).hasClass("extended")){$(section_id).removeClass("extended");}else{$(section_id).addClass("extended");}}}
function checkRMPasswordError(result,textStatus,xmlhttprequest){$('#askPasswordWindowInfoArea').text(translate('wrong_password'));$('#askPasswordWindowInfoArea').show();}
function disableRMTileParamEditing(paramKey,value){tileName=getTileParamNameByKey(paramKey);addChangeParamsObj(paramKey,RM_KEYPARAM_NAME_TYPE,value)
if(tileName!=null){if(tileName in tiles_dict){disableTile(tileName,value);}
if(tileName.substring(0,9)=='mixerTemp'){var mixerId=tileName.replace('mixerTemp','');var mixerLetter=mixerLabelLetters[mixerIds.indexOf(parseInt(mixerId))];tileName='mixerTemp'+mixerLetter;}
if($("#lbSchema_"+tileName).length!=0){disableParamOnSchema(tileName,value);}}}
function disableRMParamEditing(element_index,value){var element_key=element_index.toString();addChangeParamsObj(element_key,RM_PARAM_NAME_TYPE,value)
if(element_index<remote_menu_paramsdata.length){disableParam(element_index);}
disabledList[element_index]=value;}
function enableRMParamEditing(element_index){if(element_index<remote_menu_paramsdata.length){enableParam(element_index);}}
function enableRMTileParamEditing(paramKey){tileName=getTileParamNameByKey(paramKey);delete changedParams[paramKey];if(tileName!=null&&mixerIds!=null){if(tileName in tiles_dict){enableTile(tileName);}
if(tileName.substring(0,9)=='mixerTemp'){var mixerId=tileName.replace('mixerTemp','');var mixerLetter=mixerLabelLetters[mixerIds.indexOf(parseInt(mixerId))];tileName='mixerTemp'+mixerLetter;}
if($("#lbSchema_"+tileName).length!=0){enableParamOnSchema(tileName);}}}
function cleanRemoteMenuData(){parameters_current=null;current_params_edits=null;remote_menu_structure=null;remote_menu_paramsnames=null;remote_menu_catsnames=null;remote_menu_paramsunitsnames=null;remote_menu_paramsenums=null;remote_menu_locksnames=null;remote_menu_paramsdata=null;remote_menu_currdatadisp=null;remote_menu_paramsdescs=null;remote_menu_catsdescs=null;reg_current_parameters=null;remote_menu_alarmsnames=null;remote_menu_languages=null;shared_sections=new Object()
updater.remoteMenuVer_={}
remote_menu_current_language_version=''
remote_menu_default_language_version=''
remoteManuLang="nosel";remoteMenuDefaultLang="en";remoteMenu=false;}
function clearHistoryData(){}
function getHistoryParamValuesError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);}
function Comparator(a,b){if(a[0]<b[0])return-1;if(a[0]>b[0])return 1;return 0;}
function updateDataHistorySelectTranslation(){}
function updateDataHistorySelectTranslationET(){}
function getHistoryParamsCookies(){}
function translateHistoryParameter(param){let ptrans=param;if(EThistoryParamsNames!=null){const par=regParams[param];if(par!==undefined){ptrans=getEtTranslationByLangNum(EThistoryParamsNames[par.num]);}}else{ptrans=translateParameter(param);}
return ptrans;}
function getDateObjFromStr(dateStr,prec){if(dateStr!=undefined&&dateStr!=null){var dateArr=dateStr.split(' ')
var datePart=dateArr[0].split('-')
var timePart=null;if(dateArr.length>1){timePart=dateArr[1].split(':')}
if(datePart.length>2){var year=datePart[0]
var month=datePart[1]
var day=datePart[2]
if(timePart!=null){var hour=timePart[0]
if(prec!=null&&prec&&timePart.length>1){var min=timePart[1]
return new Date(year,month-1,day,hour,min,0);}else{return new Date(year,month-1,day,hour,0,0);}}else{return new Date(year,month-1,day,0,0,0);}}}
return(new Date())}
function hideHistoryPreloader(){}
var drawTab=[];var powerParams={"week":["Ud",7,'days'],"month":["U",31,'days'],"year":["UM",12,'months'],"years":["UR",5,'years']}
var chartEcoSolUnit="days";var chartRefreshInterval=null;var chartEcoSolOptions={series:{bars:{show:true,barWidth:0.6,align:"center",fill:0.5,},color:'#000000',},bars:{lineWidth:0,fill:true,fillColor:{colors:['#03d4ee','#48759c']},},grid:{backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:2,bottom:0,right:0},labelMargin:15},yaxis:{min:0,tickLength:0,},xaxis:{tickLength:0,tickDecimals:0,}}
function resizePlot(width){var newwidth=(width/1.5<400?400:width/1.5);var marg=(width-newwidth)/2;$("#chartMain").width(newwidth);$("#chartMain").height(newwidth/1.5);$("#chartMain").css("left",marg);$("#chartMain").css("margin-bottom",marg/2);$("#chartMain").css("margin-top",marg/2);}
function drawChart(){if(!$("#chartMain").is('DIV')||drawTab==undefined){return;}
let safety=document.getElementById("chartMainArea");if((safety===null)||(safety.offsetWidth==0)||(safety.offsetHeight==0)){return;}
resizePlot($('#chartMainArea').width())
var plot=$.plot("#chartMain",[drawTab],chartEcoSolOptions);var xaxisLabel=$("<div class='axisLabel xaxisLabel'></div>").text(translate(chartEcoSolUnit)).appendTo("#chartMain");var yaxisLabel=$("<div class='axisLabel yaxisLabel'></div>").text('kWh').appendTo("#chartMain");}
function getPowerParams(name,num){if(parameters_current!=null){drawTab=[];var currentYear=(new Date()).getFullYear();chartEcoSolOptions.xaxis.ticks=[];for(var i=1;i<=num;i++)
{if(name=='UR')
{drawTab.push([currentYear-i+1,parameters_current[name+i].value]);chartEcoSolOptions.xaxis.ticks.push(currentYear-i+1,currentYear-i+1);}
else
{drawTab.push([i,parameters_current[name+i].value]);chartEcoSolOptions.xaxis.ticks.push(i,i);}}
drawChart(drawTab,);$("#heatParamsTable").empty();addParameterBelowChart('Moc_chwilowa');addParameterBelowChart('Uzysk_ca_kowity');return true;}
return false;}
function updateChartTranslation(){$('#chartMain .xaxisLabel').text(translate(chartEcoSolUnit));$("#chartMain .xaxisLabel").css("top",$("#chartMain").height());$("#last_7_days").text(translate("last_week"));$("#current_month").text(translate("current_month"));$("#current_year").text(translate("current_year"));$("#last_years").text(translate("years"));}
function initHeatChart(){$("#yieldDaysSelectDiv").hide();if("UM1"in parameters_current){$("#rangeSelectEcoSolDiv").show();if(drawTab.length==0){yieldRangeEcoSolChange();}}
else{$("#rangeSelectEcoSolDiv").hide();chartEcoSolUnit="days"
getPowerParams("U",14);}
if(chartRefreshInterval==null)
chartRefreshInterval=setInterval(chartAutoRefresh,5000);}
function chartAutoRefresh()
{var chartRangeSelect=$('#rangeEcoSolSelect');if(chartRangeSelect!=undefined&&chartRangeSelect.is(":visible")==false&&chartRefreshInterval!=undefined&&chartRefreshInterval!=null)
{clearInterval(chartRefreshInterval);chartRefreshInterval=null;}
else
yieldRangeEcoSolChange();}
function yieldRangeEcoSolChange(){var range=$("#rangeEcoSolSelect").val();chartEcoSolUnit=powerParams[range][2];getPowerParams(powerParams[range][0],powerParams[range][1]);}
function addParameterBelowChart(param){if(parameters_current[param]!=undefined){var value=getParamValue(param,parameters_current[param].unit,parameters_current[param].mult);var value_unit=translate(PARAMETER_UNIT[parameters_current[param].unit]);$("#heatParamsTable").append('<div class="chartDescParam">'+
'<span class="chartDescParamTitle">'+translateParameter(param)+'</span>'+
'<span class="chartDescParamValue" >'+value+'</span>'+
'<span class="chartDescParamUnit" >'+value_unit+'</span>'+
'</div>');}}
var drawETTab=[];var ETticks=[];function resizeETPlot(width,height){$("#chartMain").width(width/1.5<400?400:width/1.5);$("#chartMain").height($("#chartMain").width()/1.5);drawETChart();$("#chartMain .xaxisLabel").css("top",$("#chartMain").height());}
function drawETChart(){if(!$("#chartMain").is('DIV')||drawETTab==undefined){return;}
let safety=document.getElementById("chartMain");if((safety===null)||(safety.offsetWidth==0)||(safety.offsetHeight==0)){return;}
let options={series:{bars:{show:true,barWidth:0.6,align:"center",fill:0.5,},color:'#00B4EE',},yaxis:{min:0},xaxis:{ticks:ETticks}}
var plot=$.plot("#chartMain",[drawETTab],options);if($("#yieldDaysSelect").val()>30){var xaxisLabel=$("<div class='axisLabel xaxisLabel' id='months'></div>").text(translate('months')).appendTo("#chartMain");}else{var xaxisLabel=$("<div class='axisLabel xaxisLabel' id='days'></div>").text(translate('days')).appendTo("#chartMain");}
var yaxisLabel=$("<div class='axisLabel yaxisLabel'></div>").text('kWh').appendTo("#chartMain");}
function initETHeatChart(){$("#rangeSelectEcoSolDiv").hide();$("#yieldDaysSelectDiv").show();if(drawETTab.length==0){yieldTimeRangeChange();}}
function yieldTimeRangeChange(){controller.getYieldHeats(updater.currentDevice_,$("#yieldDaysSelect").val(),getYieldHeatsResponse);}
function getYieldHeatsResponse(result,textStatus,xmlhttprequest){if(result!=undefined&&result.result!=undefined){drawETTab=[];ETticks=[];for(var item in result.result.reverse()){drawETTab.push([item,result.result[item][1]]);ETticks.push([item,result.result[item][0]]);}
resizeETPlot($(window).width(),$(window).height());}}
function translateETchart(){$("#yieldDaysLabel").text(translate("range"));$("#yieldDaysSelect option").each(function(){$(this).text(translate($(this).attr('id')));});}
var BOILER_PARAM_NAME="mode";var popup_boiler_ctrl=null;var popup_cannot_control_boiler="CANNOT_CONTROL_BOILER";var popup_can_turn_on_boiler="CAN_TURN_ON_BOILER";var popup_can_turn_off_boiler="CAN_TURN_OFF_BOILER";var paramSlider=null;var popup_weather_ctrl={"CO_TEMP_SET":"PROGRAM_CONTROL_CO","MIX_SET_TEMP_1":"CTRL_WEATHER_MIX_1","MIX_SET_TEMP_2":"CTRL_WEATHER_MIX_2","MIX_SET_TEMP_3":"CTRL_WEATHER_MIX_3","MIX_SET_TEMP_4":"CTRL_WEATHER_MIX_4","MIX_SET_TEMP_5":"CTRL_WEATHER_MIX_5"};var therm_choice_table=['THERM_CHOICE_H_1','THERM_CHOICE_H_2','THERM_CHOICE_H_3','THERM_CHOICE_H_4','THERM_CHOICE_H_5','THERM_CHOICE_H_6','THERM_CHOICE_H_7']
var PARMS_EDITS_WIN_KEYS={"editParamDataContent":["name","param_key","index","paramNum","mode_edit"],"askPasswordWindowContent":["source-section-id","data-param-title","data-param-name","name"],"twoOptPopup":["name"],"editTextTwoOptPopup":["name"],"choseOneTwoOptPopup":["name"],"updateConfTwoOptPopup":["name"]}
function validateIntegerString(minv,maxv,value){var intRegex=/^\-?\d+$/;return intRegex.test(value)&&value>=minv&&value<=maxv;}
function validateFloatString(minv,maxv,value){var parsedValue=parseFloat(value);return!isNaN(parsedValue)&&parsedValue>=minv&&parsedValue<=maxv;}
function validateBooleanString(value){return(value=="true")||(value=="false");}
function validate850iSolarParamString(value){return((parameters_current[popup_param_name].offvalue!==undefined)&&value==parameters_current[popup_param_name].offvalue)}
function validateAndShow(minv,maxv){if($('#editParamEdValue').length==0){return true}
var value=$('#editParamEdValue').text();if(minv==null&&maxv==null){return true;}
if(isFloatParam()&&validateFloatString(minv,maxv,value)){$('#editParamInfoArea').hide();return true;}else if(validateBooleanString(value)||validateIntegerString(minv,maxv,value)){$('#editParamInfoArea').hide();return true;}else if(validate850iSolarParamString(value)){$('#editParamInfoArea').hide();return true;}else{return false;}}
var popup_param_name="";var popup_title=null;function reloadEditParamWindowLabels(title){var translated_txt="";if(title!=undefined&&title!=null){$('#editParamDataWindowTitle').text(title)}else{if(popup_title){if(isDeviceGm3Conf()){if(popup_title){translated_txt=translateParameter(popup_title);popup_title=null;}}}else{if((index=$('#editParamDataContent').attr('index'))!=undefined){translated_txt=getRmParamName(index);}else if((name=$('#editParamDataContent').attr('name'))!=undefined){if(($('#editParamDataContent').attr('paramnum'))!=undefined){translated_txt=getETparamTranslation(name);}else{translated_txt=translateParameter(name);}}}
$('#editParamDataWindowTitle').text(translated_txt)}
$('#editParamSaveBtn').text(translate('save'));$('#editParamCancelBtn').text(translate('cancel'));}
function getCorrectMixerTempName(name){var lastCharacter=name.replace("mixerTemp","");var idx=mixerLabelLetters.indexOf(lastCharacter);if(idx!==-1){return"mixerTemp"+mixerIds[idx];}
return name;}
function showAlertMessagePopup(message,header){showInfoMessagePopup(message,header);}
function showInfoMessagePopup(message,header){setPopupClassOpt('#infoPopup')
$('#infoPopupContentArea').text(message);if(header!=undefined){$('#infoPopupWindowTitle').text(header);}else{$('#infoPopupWindowTitle').text(translate('remote_menu_param_edit_info'));}
$('#devicePopupBgElement').show();$('#infoPopup').show();}
function closeInfoMessagePopup(){$('#infoPopupContentArea').text("");$('#infoPopup').hide();$('#devicePopupBgElement').hide();}
function closeTwoOptPopup(){$('#twoOptPopup').hide();$('#devicePopupBgElement').hide();}
function closeEditTextTwoOptPopup(){$('#editTextTwoOptPopup').hide();$('#devicePopupBgElement').hide();}
function closeChoseOneTwoOptPopup(){$('#choseOneTwoOptPopup').hide();$('#devicePopupBgElement').hide();}
function closeUpdateConfTwoOptPopup(){$('#updateConfTwoOptPopup').hide();$('#devicePopupBgElement').hide();}
function NoSetTempPopup(header){showInfoMessagePopup(translate('temp_set_editing_off'),header)}
function WeatherCtrlPopup(header){showInfoMessagePopup(translate('weather_ctrl'),header)}
function removeEditWinKeys(windowid){for(i=0;i<PARMS_EDITS_WIN_KEYS[windowid].length;i++){$('#'+windowid).removeAttr(PARMS_EDITS_WIN_KEYS[windowid][i])}}
function reloadEditWindowKeys(windowid,keysObj){removeEditWinKeys(windowid);Object.keys(keysObj).forEach(function(key){$('#'+windowid).attr(key,keysObj[key]);});}
function prepareEnumEditWindow(select,editNameObj){reloadEditWindowKeys('editParamDataContent',editNameObj);var select_code='<div id="editParamEnumEdArea" class="greyEconetSelect editWindowPopup"><div>'+select+'</div></div>'
$('#editParamDataWindowContent').html(select_code)
$('#inpEditParamPopup').selectric('refresh');}
function prepareValueEditWindow(value,minv,maxv,precision,mult,unit,editNameObj){reloadEditWindowKeys('editParamDataContent',editNameObj);if(mult==0){mult++;}
var slider_code='<div id="editParamSliderEdArea" style="display: block;">'+
'<div id="editParamEdValueArea"><span id="editParamEdValue"></span><span id="editParamEdUnit"></span></div>'+
'<div id="sliderArea"><div id="sliderMin"><button onclick="return decPopupVal()" class="econetPlMinBtn" id="editParamOddBtn">&mdash;</button><span id="editParamMinVal">min 1°C</span></div>'+
'<div id="sliderContent"><div id="slider-param"></div></div>'+
'<div id="sliderMax"><button onclick="return incPopupVal()" class="econetPlMinBtn" id="editParamAddBtn">+</button><span id="editParamMaxVal"></span></div>'+
'</div></div>';$('#editParamDataWindowContent').html(slider_code)
$('#editParamEdUnit').text(unit);$('#editParamMinVal').text("min "+convertValToStr(minv)+unit)
$('#editParamMaxVal').text("max "+convertValToStr(maxv)+unit)
if(paramSlider!=null&&paramSlider.noUiSlider!=undefined){paramSlider.noUiSlider.destroy()}
paramSlider=document.getElementById('slider-param');noUiSlider.create(paramSlider,{start:value,step:mult,range:{'min':minv,'max':maxv}});var paramField=$('#editParamEdValue');paramSlider.noUiSlider.on('update',function(values,handle){paramField.text(parseFloat(values[handle]).toFixed(precision));});}
function EnumPopup(popup_param_name,mult,minIndex,maxIndex,value,popupEditName,popupEditMode){var select='<select id="inpEditParamPopup" class="popupSelection">';var i=0;for(k in ENUM_TYPE[mult]){if(minIndex!=null&&k<minIndex){++i;continue;}
if(maxIndex!=null&&k>maxIndex){break;}
select+='<option value="'
+i
+'" '
+(value==i?'selected="selected"':'')
+'">'
+(mult!=106?translate(ENUM_TYPE[mult][k]):ENUM_TYPE[mult][k])+'</option>';++i;}
select+="</select>";var winParams={'name':popupEditName};if(popupEditMode!=undefined&&popupEditMode){winParams['mode_edit']=true}
prepareEnumEditWindow(select,winParams)}
function UsualPopup(popup_param_name,popupEditName){var editParam=parameters_current[popup_param_name];var precision=getNumberPrecision(editParam.mult);var currvalue=editParam.value
var minValue=editParam.minv
var maxValue=editParam.maxv
if((editParam.offvalue!==undefined)&&editParam.value==editParam.offvalue){currvalue=translate('0');$('#editParamEdUnit').hide();}else{$('#editParamEdUnit').show();}
prepareValueEditWindow(currvalue,minValue,maxValue,precision,editParam.mult,translate(PARAMETER_UNIT[editParam.unit]),{'name':popupEditName})}
function popupParamETeditable(editableParamNum){var editableParam=ETeditableParams[editableParamNum]
var paramNum=editableParam[0];var editParam=ETparametersData[paramNum];var row=null;var paramName=editParam.name;if(changedParams[paramName]!=undefined){return;}
popup_param_name=paramName;var paramUnit=editableParam[1];var currvalue=editParam.value
var minValue=editParam.minv
var maxValue=editParam.maxv
var mult=editParam.mult
var version='version'
var multiply=null
if((ETconfigEditableParams!=null)&&(editableParamNum in ETconfigEditableParams)){row=ETconfigEditableParams[editableParamNum];if(row[0]==paramNum){if(3 in row&&row[3]!=null){minValue=row[3];}
if(4 in row&&row[4]!=null){maxValue=row[4];}
if(5 in row&&row[5]!=null){mult=row[5];}}}
if(ETconfigEditableParamsMulti!=null){for(var i in ETconfigEditableParamsMulti){row=ETconfigEditableParamsMulti[i];if(row[0]==paramNum){multiply=row[1];currvalue*=multiply;currvalue=currvalue.toFixed(5);currvalue=parseFloat(currvalue);break;}}}
if((editableParam.length>3)&&(editableParam[3]!=null)){minValue=editableParam[3]}
if((editableParam.length>4)&&(editableParam[4]!=null)){maxValue=editableParam[4]}
if((editableParam.length>5)&&(editableParam[5]!=null)){mult=editableParam[5]}
var precision=getNumberPrecision(mult);$('#editParamEdUnit').show();prepareValueEditWindow(currvalue,minValue,maxValue,precision,mult,getParamUnitStr(paramUnit),{'name':("editableParam"+editableParamNum),'paramNum':paramNum})
openEditParamPopup();}
function popupParamETeditableTile(paramNum,title,fParamName,edParamNum){var editParam=ETparametersData[paramNum];var paramName=editParam.name;if(changedParams[paramName]!=undefined){return;}
popup_param_name=paramName;var attrName=''
if(title!=null){attrName=title;}else{if(paramsETtranslations!=null&&fParamName!=null){if(paramsETtranslations[fParamName]!=undefined){attrName=paramsETtranslations[fParamName];}}}
if(edParamNum!=undefined&&edParamNum!=null&&ETeditableParams[edParamNum]!=undefined){var paramUnit=ETeditableParams[edParamNum][1];}else{var paramUnit=editParam.unit;}
var precision=getNumberPrecision(editParam.mult);var currvalue=editParam.value
var minValue=editParam.minv
var maxValue=editParam.maxv
$('#editParamEdUnit').show();prepareValueEditWindow(currvalue,minValue,maxValue,precision,editParam.mult,getParamUnitStr(paramUnit),{'name':attrName,'paramNum':paramNum})
openEditParamPopup();}
function popupParamETbit(choiceParamNum){var paramNum=ETchoiceParams[choiceParamNum][0];var choiceParam=ETparametersData[paramNum];var paramName=choiceParam.name;if(changedParams[paramName]!=undefined){return;}
popup_param_name=paramName;var select='<select id="inpEditParamPopup" class="popupSelection">';var paramVal=choiceParam.value;var settings=ETchoiceParams[choiceParamNum][1];var valueName=getParamBitValue(paramVal,settings);for(var item in settings){var value=paramVal|settings[item][0];value=(value&(~settings[item][1]))>>>0;select+='<option value="'+value+'" '
+(valueName==item?'selected="selected"':'')+'">'
+translateBitValue("choiceParam"+choiceParamNum,item)
+'</option>';}
select+="</select>";prepareEnumEditWindow(select,{'name':("choiceParam"+choiceParamNum),'paramNum':paramNum})
openEditParamPopup();}
function openEditParamPopup(title){reloadEditParamWindowLabels(title);$('#editParamSaveBtn').prop("disabled",false);showEditWindow('#secEditParamData')}
function showEditWindow(windowid){$('#deviceBgElement').hide()
$(windowid).siblings('[id^="sec"]').hide();$(windowid).show();}
function closeEditWindow(id){if($(id).is(':visible')){reloadEditWindowKeys('editParamDataContent',{});if(paramSlider!=null&&paramSlider.noUiSlider!=undefined){paramSlider.noUiSlider.destroy()}
var click=false;$('#mainMenu #tabs').children().each(function(){if($(this).hasClass('current')){$(this).trigger("click");click=true;return;}});if(!click){$('#tabHrData').trigger("click");}}}
function popupParam(param,title,mode_edit){reloadEditWindowKeys('editParamDataContent',{});popup_param_name=null;if(param.substring(0,9)=="mixerTemp"){param=getCorrectMixerTempName(param);}
if(current_params_edits!=null&&remote_menu_currdatadisp!=null&&(RM_PARAMETERS_CONN[param]!=undefined||(parameters_current!=undefined&&parameters_current!=null&&parameters_current[param]==undefined&&RM_PARAMETERS_850I_CONN[param]!=undefined))){if(controller.type_==ECOMAX_850i_TYPE){popup_param_key=RM_PARAMETERS_850I_CONN[param];}else{popup_param_key=RM_PARAMETERS_CONN[param];}
if(changedParams[popup_param_key]!=undefined){return;}
rmTilesPopupParam(popup_param_key,title)}else{var pconn=PARAMETERS_CONN[param];if(pconn!=undefined&&pconn!=null){if(pconn.length>2){popup_param_name=getSelectionParam(param);}else{popup_param_name=PARAMETERS_CONN[param][controller.type_];}}else{popup_param_name=param;}
if(title&&title.length>0){var popup_edit_name=title}else{var popup_edit_name=popup_param_name}
if((popup_param_name=="")&&(param=="ecoSterTemp1")&&(ngDevNfo.get_brand()==48)&&(ngDevNfo.get_ver_mod_a()=="4.34.46.K1")&&(ngDevNfo.get_protocol()=="em")){rmPopupParam('38','79');return;}
if(changedParams[popup_param_name]!=undefined&&(popup_param_name=="mode"&&$("#tilesCanvas_mode").parent().hasClass('tilemodedisabled'))){if(popup_param_name!="mode"){return;}
if(popup_param_name=="mode"&&$("#tilesCanvas_mode").parent().hasClass('tilemodedisabled')){return;}}
if(param==BOILER_PARAM_NAME&&controller.protocol_type=='em'){popupBoilerCtrl();return;}else if(parameters_current[popup_param_name]!=null&&!isUserParamSection(parameters_current[popup_param_name].sec)&&typeof devices_dict!=='undefined'&&!devices_dict[updater.currentDevice_].serviceParamsEdit&&isNormalUser()){showAlertMessagePopup(translate('service_password_msg'),translate(popup_param_name));return;}else if(parameters_current[popup_param_name]!=null&&!shouldShowParam(popup_param_name)){NoSetTempPopup(translate(popup_param_name));return;}else if(popup_weather_ctrl[popup_param_name]!=null&&parameters_current[popup_weather_ctrl[popup_param_name]]!=null&&parameters_current[popup_weather_ctrl[popup_param_name]].value!=0){WeatherCtrlPopup(translateParameter(popup_param_name));return;}else if(parameters_current[popup_param_name]!=null&&parameters_current[popup_param_name].unit==ENUM_UNIT){var mult=parameters_current[popup_param_name].mult;var maxIndex=parameters_current[popup_param_name].maxv;var minIndex=parameters_current[popup_param_name].minv;EnumPopup(popup_param_name,mult,minIndex,maxIndex,parameters_current[popup_param_name].value,popup_edit_name,mode_edit);}else{UsualPopup(popup_param_name,popup_edit_name);}
openEditParamPopup();}}
function closePopup(popupDiv){$('#'+popupDiv).hide();$('#devicePopupBgElement').hide();return false;}
function closeAllPopups(){disableTileMode=false;closeEditWindow('#secEditParamData');closeEditWindow('#secAskServicePassword')
closeInfoMessagePopup();closeTwoOptPopup();closeEditTextTwoOptPopup();closeChoseOneTwoOptPopup();closeUpdateConfTwoOptPopup();}
function savePopupParam(){if($('#editParamDataContent').attr('mode_edit')&&$('#editParamDataContent').attr('mode_edit').indexOf("true")!=-1){disableTileMode=true;}else{disableTileMode=false;}
if($('#editParamDataContent').attr('index')){var element_index=$('#editParamDataContent').attr('index');var param_descr=getRmParamData(element_index)
if(param_descr!=null){if(validateAndShow(param_descr.minv,param_descr.maxv)||param_descr.unit==ENUM_UNIT){var val=getPopupParamValue();if(val==null)
return;if(typeof param_descr.value=='boolean')
val=val==0?false:true;controller.rmSaveParam(element_index,val,savePopupParamResponse,savePopupParamError);if(!(isMemberOfGroup(GROUP_SERVICE)&&updater.serviceAccess_!=SERVICE_MODIFY)){disableRMParamEditing(element_index,val);}}}}else if($('#editParamDataContent').attr('param_key')){var param_key=$('#editParamDataContent').attr('param_key');var param_disp=getRmCurrDisp(param_key)
var param_edit=getRmCurrEdit(param_key)
if(validateAndShow(param_edit.min,param_edit.max)||param_edit.unit==ENUM_UNIT){var val=getPopupParamValue();if(val==null)
return;controller.rmSaveCurrParam(param_key,val,savePopupParamResponse,savePopupParamError);if(!(isMemberOfGroup(GROUP_SERVICE)&&updater.serviceAccess_!=SERVICE_MODIFY)){disableRMTileParamEditing(param_key,val);}}}else{if(popup_param_name==BOILER_PARAM_NAME){setBoilerMode();closeTwoOptPopup();}else if($('#editParamDataContent').attr('paramNum')){var paramNum=$('#editParamDataContent').attr('paramNum');var val=getPopupParamValue();if(val==null)
return;if(ETconfigEditableParamsMulti!=null){for(var i in ETconfigEditableParamsMulti){row=ETconfigEditableParamsMulti[i];if(row[0]==paramNum){multiply=row[1];val/=multiply;val=val.toFixed(5);val=parseFloat(val);break;}}}
controller.saveParam(paramNum,val,savePopupParamResponse,savePopupParamError);disableParamEditing(ETparametersData[paramNum].name,val,paramNum);}else if(parameters_current!=null&&parameters_current[popup_param_name]!=null){if(validateAndShow(parameters_current[popup_param_name].minv,parameters_current[popup_param_name].maxv)||parameters_current[popup_param_name].unit==ENUM_UNIT){var val=getPopupParamValue();if(val==null)
return;if(typeof parameters_current[popup_param_name].value=='boolean')
val=val==0?false:true;if(controller.protocol_type=="em")
controller.saveParam(popup_param_name,val,savePopupParamResponse,savePopupParamError);else{if(popup_param_name in parameters_current)
controller.saveParam(parameters_current[popup_param_name].num,val,savePopupParamResponse,savePopupParamError);}
if(!(isMemberOfGroup(GROUP_SERVICE)&&updater.serviceAccess_!=SERVICE_MODIFY)){disableParamEditing(popup_param_name,val);}}}else{console.log("savePopupParam(): parameter '"+popup_param_name+"' boundaries not available!");}}
$('#editParamSaveBtn').prop("disabled",true);return false;}
function getPopupParamValue(){if($('#editParamEdValue').length>0){return $('#editParamEdValue').text()}else if($('#inpEditParamPopup').length>0){return $('#inpEditParamPopup').val();}else{return null;}}
function showConfirmLabelAndClose(lbName,popupDiv){$('#'+lbName).text(translate('changes_saved'));$('#'+lbName).attr('class','infoLabel');$('#'+lbName).show();setTimeout(function(){$('#'+lbName).hide();closePopup(popupDiv);},Parameters.HIDE_CONFIRM_DELAY);}
function showEditParamConfirmLabelAndClose(lbName,windowid){$(lbName).text(translate('changes_saved'));$(lbName).attr('class','infoLabel');$(lbName).show();setTimeout(function(){$(lbName).hide();closeEditWindow(windowid);},Parameters.HIDE_CONFIRM_DELAY);}
function showError(lbName,text){var infoLabel=$('#'+lbName);infoLabel.attr("class","errLabel");if(text!=undefined)
infoLabel.text(translate(text));else
infoLabel.text(translate("save_error"));infoLabel.show();}
function updateParamSliderValue(value){if(paramSlider!=null&&paramSlider.noUiSlider!=undefined){paramSlider.noUiSlider.set([value,null]);}}
function savePopupParamResponse(result,textStatus,xmlhttprequest){if(result.hasOwnProperty("error")){showError('editParamInfoArea',result.error);return;}
if($('#editParamSliderEdArea').is(':visible')){updateParamSliderValue(result.paramValue)}
showEditParamConfirmLabelAndClose('#editParamInfoArea','#secEditParamData');}
function savePopupParamError(result,textStatus,xmlhttprequest){showError('paramInfoPopup');}
function isFloatParam(){if($('#editParamDataContent').attr('index')){var element_index=$('#editParamDataContent').attr('index');var param_descr=getRmParamData(element_index)
return(getNumberPrecision(param_descr.mult)>0);}else if($('#editParamDataContent').attr('param_key')){var param_key=$('#editParamDataContent').attr('param_key');var param_disp=getRmCurrDisp(param_key)
var param_edit=getRmCurrEdit(param_key)
var precision=getNumberPrecision(param_disp.special);return(precision>0);}else{var val=parameters_current[$('#editParamDataContent').attr('name')].mult;return(getNumberPrecision(val)>0);}
return false;}
function getMaxFromParamDescription(paramName,paramKey){const parEditableIndex=parseInt(paramName.replace(paramKey,""))
const edParam=ETeditableParams[parEditableIndex]
if(edParam!=undefined&&edParam!=null&&edParam.length>4){return edParam[4]}
return null}
function getMinFromParamDescription(paramName,paramKey){const parEditableIndex=parseInt(paramName.replace(paramKey,""))
const edParam=ETeditableParams[parEditableIndex]
if(edParam!=undefined&&edParam!=null&&edParam.length>3){return edParam[3]}
return null}
function getStepFromParamDescription(paramName,paramKey){const parIdx=parseInt(paramName.replace(paramKey,""))
if((ETconfigEditableParams!==null)&&(ETconfigEditableParams!==undefined)&&(parIdx in ETconfigEditableParams)){const edParam=ETconfigEditableParams[parIdx];if((5 in edParam)&&(edParam[5]!=null)){return edParam[5];}}
if((ETeditableParams!==null)&&(ETeditableParams!==undefined)&&(parIdx in ETeditableParams)){const edParam=ETeditableParams[parIdx];if((5 in edParam)&&(edParam[5]!=null)){return edParam[5];}
var dpIdx=edParam[0];if((ETparametersData!==null)&&(ETparametersData!==undefined)&&(dpIdx in ETparametersData)){return ETparametersData[dpIdx].mult;}}
return null}
function incPopupVal(){var param_name=$('#editParamDataContent').attr('name');if($('#editParamDataContent').attr('index')){var element_index=$('#editParamDataContent').attr('index');var param_descr=getRmParamData(element_index)
var precision=getNumberPrecision(param_descr.mult);var newVal=parseFloat($('#editParamEdValue').text());if(newVal<param_descr.maxv){newVal=(newVal+param_descr.mult).toFixed(precision);}}else if($('#editParamDataContent').attr('param_key')){var param_key=$('#editParamDataContent').attr('param_key');var param_disp=getRmCurrDisp(param_key)
var param_edit=getRmCurrEdit(param_key)
var precision=getNumberPrecision(param_disp.special);var newVal=parseFloat($('#editParamEdValue').text());if(newVal<param_edit.max){newVal=(newVal+1).toFixed(precision);}}else if($('#editParamDataContent').attr('paramNum')){var paramNum=$('#editParamDataContent').attr('paramNum');var newVal=parseFloat($('#editParamEdValue').text());var paramName=$('#editParamDataContent').attr('name');var maxVal=getMaxFromParamDescription(paramName,"editableParam")
if(maxVal==null){maxVal=ETparametersData[paramNum].maxv}
var mult=getStepFromParamDescription(paramName,"editableParam")
if(mult==null){mult=ETparametersData[paramNum].mult}
var precision=getNumberPrecision(mult);if(maxVal==null||newVal<maxVal){newVal=(newVal+mult).toFixed(precision);}}else{var precision=getNumberPrecision(parameters_current[param_name].mult);var newVal=parseFloat($('#editParamEdValue').text());if(parameters_current[param_name].maxv==null||newVal<parameters_current[param_name].maxv){if(PARAMETERS_INCREASED_BY_2.indexOf(param_name)>-1)
newVal=(newVal+2).toFixed(precision);else if((parameters_current[param_name].offvalue!==undefined)&&(newVal==parameters_current[param_name].offvalue)){$('#editParamEdUnit').show()
newVal=(parameters_current[param_name].minv).toFixed(precision);}else
newVal=(newVal+parameters_current[param_name].mult).toFixed(precision);}}
updateParamSliderValue(newVal)
return false;}
function decPopupVal(){var param_name=$('#editParamDataContent').attr('name');if($('#editParamDataContent').attr('index')){var element_index=$('#editParamDataContent').attr('index');var param_descr=getRmParamData(element_index)
var precision=getNumberPrecision(param_descr.mult);var newVal=parseFloat($('#editParamEdValue').text());if(newVal>param_descr.minv){newVal=(newVal-param_descr.mult).toFixed(precision);}}else if($('#editParamDataContent').attr('param_key')){var param_key=$('#editParamDataContent').attr('param_key');var param_disp=getRmCurrDisp(param_key)
var param_edit=getRmCurrEdit(param_key)
var precision=getNumberPrecision(param_disp.special);var newVal=parseFloat($('#editParamEdValue').text());if(newVal>param_edit.min){newVal=(newVal-1).toFixed(precision);}}else if($('#editParamDataContent').attr('paramNum')){var paramNum=$('#editParamDataContent').attr('paramNum');var newVal=parseFloat($('#editParamEdValue').text());var paramName=$('#editParamDataContent').attr('name');var minVal=getMinFromParamDescription(paramName,"editableParam")
if(minVal==null){minVal=ETparametersData[paramNum].minv}
var mult=getStepFromParamDescription(paramName,"editableParam")
if(mult==null){mult=ETparametersData[paramNum].mult}
var precision=getNumberPrecision(mult);if(minVal==null||newVal>minVal){newVal=(newVal-mult).toFixed(precision);}}else{var precision=getNumberPrecision(parameters_current[param_name].mult);var newVal=parseFloat($('#editParamEdValue').text());if(parameters_current[param_name].minv==null||newVal>parameters_current[param_name].minv){if(PARAMETERS_INCREASED_BY_2.indexOf(param_name)>-1)
newVal=(newVal-2).toFixed(precision);else
newVal=(newVal-parameters_current[param_name].mult).toFixed(precision);}else if(parameters_current[param_name].offvalue!==undefined){$('#editParamEdValue').text(translate('0'));$('#editParamEdUnit').hide()
newVal=parameters_current[param_name].offvalue;}}
updateParamSliderValue(newVal)
return false;}
function inpEditParamPopupCheckboxChanged(){var inp=$('#inpEditParamPopup');inp.val(inp.is(':checked'));}
function openTwoOptPop(){$('#devicePopupBgElement').show();$('#twoOptPopup').show();}
function openEditTextTwoOptPop(){$('#devicePopupBgElement').show();$('#editTextTwoOptPopup').show();}
function openChoseOneTwoOptPop(){$('#devicePopupBgElement').show();$('#choseOneTwoOptPopup').show();}
function openUpdateConfTwoOptPop(){$('#devicePopupBgElement').show();$('#updateConfTwoOptPopup').show();}
function popupBoilerCtrl(){$('#twoOptPopupWindowTitle').text(translateParameter('mode'));$("#twoOptPopupOK").text(translate('yes'));$("#twoOptPopupCancel").text(translate('no'));if(popup_boiler_ctrl==popup_can_turn_on_boiler){if(controller.type_==ECOMAX_850i_TYPE){$('#twoOptPopupContentArea').text(translate('regulator_control_on'));}else{$('#twoOptPopupContentArea').text(translate('boiler_control_on'));}}else if(popup_boiler_ctrl==popup_can_turn_off_boiler){if(controller.type_==ECOMAX_850i_TYPE){$('#twoOptPopupContentArea').text(translate('regulator_control_off'));}else{$('#twoOptPopupContentArea').text(translate('boiler_control_off'));}}else{console.log("popupBoilerCtrl(): Error wrong popup_boiler_ctrl state: "
+popup_boiler_ctrl);}
prepareTwoOptPopup("savePopupParam();","closeTwoOptPopup(); return false;",{"name":"mode"})
openTwoOptPop();}
function setBoilerModeResponse(result,textStatus,xmlhttprequest){if(result.hasOwnProperty("error")){showError('paramInfoPopup',result.error);return;}
showConfirmLabelAndClose('paramInfoPopup','chgParamPopup');}
function setBoilerModeError(jqXHR,textStatus,errorThrown){showError('paramInfoPopup');}
function setBoilerMode(){if(popup_boiler_ctrl==popup_can_turn_on_boiler){controller.saveParam('BOILER_CONTROL',1,setBoilerModeResponse,setBoilerModeError);changedParams["mode"]=3;disableTile("mode",3);}else if(popup_boiler_ctrl==popup_can_turn_off_boiler){controller.saveParam('BOILER_CONTROL',0,setBoilerModeResponse,setBoilerModeError);changedParams["mode"]=0;disableTile("mode",0);}else{console.log("setBoilerMode(): Error wrong popup_boiler_ctrl state!");}}
function setPopupClassOpt(popupid){if($('#deviceLeftPanelNavArea').is(':visible')&&!$('#aMenu').is(':visible')){$(popupid).attr("class","econetPopupLM");}else{$(popupid).attr("class","econetPopup");}}
function openDeviceRestartWarningPopup(){$('#twoOptPopupWindowTitle').text(translate('restart_device'));$('#twoOptPopupContentArea').text(translate('restart_device_warning'));$("#twoOptPopupOK").text(translate('yes'));$("#twoOptPopupCancel").text(translate('no'));prepareTwoOptPopup("restartDevice();","closeTwoOptPopup();",{})
openTwoOptPop();}
function openSaveListsWarningPopup(){$('#twoOptPopupWindowTitle').text(translate('save_lists_popup'));$('#twoOptPopupContentArea').text(translate('save_lists_warning'));$("#twoOptPopupOK").text(translate('yes'));$("#twoOptPopupCancel").text(translate('no'));prepareTwoOptPopup("saveEconetBlWhLists(); closeTwoOptPopup();","closeTwoOptPopup();",{})
openTwoOptPop();}
function openUpdateSoftPopup(){$('#twoOptPopupWindowTitle').text(translate('update_software'));$('#twoOptPopupContentArea').text(translate('update_confirm'));$("#twoOptPopupOK").text(translate('yes'));$("#twoOptPopupCancel").text(translate('no'));prepareTwoOptPopup("updateProcessConf();","closeTwoOptPopup(); return false;",{"name":"update_software"})
openTwoOptPop();}
function updateProcessConf(){startUpdateProcess();closeTwoOptPopup();}
function openUpdateKeyPopup(macUid,key){var macArr=macUid.split(";");var mac=macArr[0];var uid=macArr[1];$('#editTextTwoOptPopupWindowTitle').text(translate('Update_key')+" ("+uid+")");var text='<label><strong>'+translate("devicesMac")+'</strong></label><label>'+mac+'</label></br> '+
'<div id="editTextTwoOptPopupKeyArea"> '+
'	<label id="editTextTwoOptPopupKeyTitle">Key</span> '+
'	<input type="text" name="editTextTwoOptPopupKeyInput" id="editTextTwoOptPopupKeyInput" class="econetEditPasswordField" readonly> '+
'</div> '+
'<label>'+translate("write_new_signature")+'</label>'
$('#editTextTwoOptPopupContentArea').html(text);$('#editTextTwoOptPopupKeyInput').val(key);$('#editTextTwoOptPopupInput').val("");$("#editTextTwoOptPopupOK").text(translate('OK'));$("#editTextTwoOptPopupCancel").text(translate('cancel'));prepareEditTextTwoOptPopup("updateKey($('#editTextTwoOptPopupInput').val(),'"+uid+"');","closeEditTextTwoOptPopup(); return false;",{"name":"update_key"})
openEditTextTwoOptPop();}
function openUpdateConfirmPopup(oldSW,newSW,moduleName){$("#oldSW").html(oldSW);$("#newSW").html(newSW);$('#updateConfTwoOptPopupWindowTitle').text(translate('conf_popup_title'));if(moduleName!=undefined){$("#updConfModuleName").html(moduleName);}
$("#updateConfTwoOptPopupOK").text(translate('OK'));$("#updateConfTwoOptPopupCancel").text(translate('cancel'));prepareUpdateConfTwoOptPopup("confirmUpdateProcess();","cancelUpdate(); closeUpdateConfTwoOptPopup(); return false;",{"name":"confirm_update"})
openUpdateConfTwoOptPop();}
function popupModeOnlyParam(tile_param_name){var tile=tiles_dict[tile_param_name];if(tile!=null&&tile!=undefined){var mode_param_name='';var add_params=tile.extra_.addParameters.split(';')
var index=tile.extra_.index
if(tile.type_==tiles_type_temp_wave&&index!=undefined&&index!=null&&parameters_current!=null){for(var i=0;i<therm_choice_table.length;i++){var therm_choice=therm_choice_table[i]
if(parameters_current!=null&&therm_choice in parameters_current){if(parameters_current[therm_choice].value.toString()==index){mode_param_name=STER_MODE_PARAM[controller.type_]+(i+1)
break;}}}}else if(THERM_MODE_EDIT_TILES.length==OTHER_MODE_EDITS.length&&THERM_MODE_EDIT_TILES.indexOf(tile.memberName_)!=-1){mode_param_name=OTHER_MODE_EDITS[THERM_MODE_EDIT_TILES.indexOf(tile.memberName_)]}else{for(var i=0;i<add_params.length;i++){if(add_params[i].indexOf(STER_MODE_PARAM[controller.type_])!=-1){mode_param_name=add_params[i];break;}}}
if(mode_param_name!=''){popupParam(mode_param_name,mode_param_name,true)}else{return;}}else{return;}}
function popupModeEditParam(tile_param_name){var tile=tiles_dict[tile_param_name];if(tile!=null&&tile!=undefined){var main_param_id=''
var main_param_name=''
var html_list=''
if((tile.extra_&&tile.extra_.addParameters)&&parameters_current!=null){var index=tile.extra_.index;var curr_mode_value=parameters_current[STER_MODE_PARAM[controller.type_]
+index]
var tmp_param_name=''
main_param_id='STER_TEMP';if(tile.type_==tiles_type_temp){main_param_name=tile_param_name;}else{if(curr_mode_value!=undefined&&curr_mode_value.value<STER_TEMP_PARAMS_MAP[controller.type_].length){tmp_param_name=STER_TEMP_PARAMS_MAP[controller.type_][curr_mode_value.value]
if(tmp_param_name=="harm"&&regParams!=null){var temp_selection_param=tile.extra_.tempSelection;var contact=regParams[temp_selection_param]
if(contact!=undefined){if(contact.val){main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][2]
+index}else{if(controller.type_==0)
main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][1]
+index
if(controller.type_==1)
main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][3]
+index}}}else if(tmp_param_name=="harmdn"&&regParams!=null){var temp_selection_param=tile.extra_.tempSelection;var contact=regParams[temp_selection_param]
if(contact!=undefined){if(contact.val){main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][2]
+index}else{main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][4]
+index}}}else{if(tmp_param_name.length>0){main_param_name=tmp_param_name+index}}}}}
var mode_param_name='';var add_params=tile.extra_.addParameters.split(';')
for(var i=0;i<add_params.length;i++){if(add_params[i].indexOf(STER_MODE_PARAM[controller.type_])!=-1){mode_param_name=add_params[i];break;}}
if(mode_param_name!=''){popupParam(mode_param_name,mode_param_name,true)}else{return;}}else{return;}}
function preparePasswordPopup(submitfun,cancelfun,keypressfun,editNameObj){reloadEditWindowKeys('askPasswordWindowContent',editNameObj);if(submitfun!=null){$('#popupPasswdOK').attr("onclick",submitfun);}else{$('#popupPasswdOK').removeAttr("onclick")}
if(cancelfun!=null){$('#popupPasswdCancel').attr("onclick",cancelfun);}else{$('#popupPasswdCancel').removeAttr("onclick")}
if(keypressfun!=null){$('#inpServicePasswd').attr("onkeypress",keypressfun);}else{$('#inpServicePasswd').removeAttr("onkeypress")}
$('#askPasswordWindowInfoArea').text("");$('#askPasswordWindowInfoArea').hide();$('#inpServicePasswd').val("");}
function prepareTwoOptPopup(submitfun,cancelfun,editNameObj){reloadEditWindowKeys('twoOptPopup',editNameObj);setPopupClassOpt('#twoOptPopup')
if(submitfun!=null){$('#twoOptPopupOK').attr("onclick",submitfun);$('#twoOptPopupOK').show();}else{$('#twoOptPopupOK').removeAttr("onclick")
$('#twoOptPopupOK').hide();}
if(cancelfun!=null){$('#twoOptPopupCancel').attr("onclick",cancelfun);$('#twoOptPopupCancel').show();}else{$('#twoOptPopupCancel').removeAttr("onclick")
$('#twoOptPopupCancel').hide();}}
function prepareEditTextTwoOptPopup(submitfun,cancelfun,editNameObj){reloadEditWindowKeys('editTextTwoOptPopup',editNameObj);setPopupClassOpt('#editTextTwoOptPopup')
if(submitfun!=null){$('#editTextTwoOptPopupOK').attr("onclick",submitfun);$('#editTextTwoOptPopupOK').show();}else{$('#editTextTwoOptPopupOK').removeAttr("onclick")
$('#editTextTwoOptPopupOK').hide();}
if(cancelfun!=null){$('#editTextTwoOptPopupCancel').attr("onclick",cancelfun);$('#editTextTwoOptPopupCancel').show();}else{$('#editTextTwoOptPopupCancel').removeAttr("onclick")
$('#editTextTwoOptPopupCancel').hide();}}
function prepareChoseOneTwoOptPopup(submitfun,cancelfun,editNameObj){reloadEditWindowKeys('choseOneTwoOptPopup',editNameObj);setPopupClassOpt('#choseOneTwoOptPopup')
if(submitfun!=null){$('#choseOneTwoOptPopupOK').attr("onclick",submitfun);$('#choseOneTwoOptPopupOK').show();}else{$('#choseOneTwoOptPopupOK').removeAttr("onclick")
$('#choseOneTwoOptPopupOK').hide();}
if(cancelfun!=null){$('#choseOneTwoOptPopupCancel').attr("onclick",cancelfun);$('#choseOneTwoOptPopupCancel').show();}else{$('#choseOneTwoOptPopupCancel').removeAttr("onclick")
$('#choseOneTwoOptPopupCancel').hide();}}
function prepareUpdateConfTwoOptPopup(submitfun,cancelfun,editNameObj){reloadEditWindowKeys('updateConfTwoOptPopup',editNameObj);setPopupClassOpt('#updateConfTwoOptPopup')
if(submitfun!=null){$('#updateConfTwoOptPopupOK').attr("onclick",submitfun);$('#updateConfTwoOptPopupOK').show();}else{$('#updateConfTwoOptPopupOK').removeAttr("onclick")
$('#updateConfTwoOptPopupOK').hide();}
if(cancelfun!=null){$('#updateConfTwoOptPopupCancel').attr("onclick",cancelfun);$('#updateConfTwoOptPopupCancel').show();}else{$('#updateConfTwoOptPopupCancel').removeAttr("onclick")
$('#updateConfTwoOptPopupCancel').hide();}}
function getSelectionParam(tile_param_name){var tile=tiles_dict[tile_param_name];if(tile!=null&&tile!=undefined){var main_param_id=''
var main_param_name=''
if((tile.extra_&&tile.extra_.addParameters)&&parameters_current!=null){var index=tile.extra_.index;var curr_mode_value=parameters_current[STER_MODE_PARAM[controller.type_]+index]
var tmp_param_name=''
main_param_id='STER_TEMP';if(tile.type_==tiles_type_temp){main_param_name=tile_param_name;edit=false;}else{if(curr_mode_value!=undefined&&curr_mode_value.value<STER_TEMP_PARAMS_MAP[controller.type_].length){tmp_param_name=STER_TEMP_PARAMS_MAP[controller.type_][curr_mode_value.value]
if(tmp_param_name=="harm"&&regParams!=null){var temp_selection_param=tile.extra_.tempSelection;var contact=regParams[temp_selection_param]
if(contact!=undefined){if(contact.val){main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][2]+index}else{if(controller.type_==0)
main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][1]+index
if(controller.type_==1)
main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][3]+index}}}else if(tmp_param_name=="harmdn"&&regParams!=null){var temp_selection_param=tile.extra_.tempSelection;var contact=regParams[temp_selection_param]
if(contact!=undefined){if(contact.val){main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][2]+index}else{main_param_name=STER_TEMP_PARAMS_MAP[controller.type_][4]+index}}}else{if(tmp_param_name.length>0){main_param_name=tmp_param_name+index}}}}}}
return main_param_name;}
function RMEnumPopup(element_index,param_descr){var select='<select id="inpEditParamPopup" class="popupSelection">';var offset=param_descr.offset;if(offset<remote_menu_paramsenums.length){var enum_element=remote_menu_paramsenums[offset]
var enum_first=enum_element.first
var enum_values=enum_element.values
var maxIndex=param_descr.maxv-enum_first;var minIndex=param_descr.minv-enum_first;var i=0;for(k in enum_values){if(minIndex!=null&&k<minIndex){++i;continue;}
if(maxIndex!=null&&k>maxIndex){break;}
select+='<option value="'+i+'" '+(param_descr.value==i?'selected="selected"':'')+'">'+
enum_values[k]+
'</option>';++i;}
select+="</select>";}
prepareEnumEditWindow(select,{'index':element_index})}
function RMUsualPopup(element_index,param_descr){var precision=getNumberPrecision(param_descr.mult);prepareValueEditWindow(param_descr.value,param_descr.minv,param_descr.maxv,precision,param_descr.mult,getRmParamValueUnit(element_index),{'index':element_index})}
function RMCurrentUsualPopup(element_key,param_disp,param_edit){var precision=getNumberPrecision(param_disp.special);prepareValueEditWindow(param_edit.value,param_edit.min,param_edit.max,precision,param_disp.special,getRmUnitByIndex(param_disp.unit),{'param_key':element_key})}
function RMLockPopup(lock_index,title){showAlertMessagePopup(getRmLockName(lock_index),title);}
function rmPopupParam(structure_index,param_index){if(changedParams[param_index.toString()]!=undefined){return;}
popup_param_name=getRmParamName(param_index);var param_descr=getRmParamData(param_index)
if(param_descr!=null){if(isLockElement(structure_index)){RMLockPopup(getLockIndex(structure_index),popup_param_name)
return;}else{if(param_descr.unit==ENUM_UNIT){RMEnumPopup(param_index,param_descr);}else{RMUsualPopup(param_index,param_descr);}}}
openEditParamPopup();}
function rmTilesPopupParam(param_key,tile){var param_disp=getRmCurrDisp(param_key)
var param_edit=getRmCurrEdit(param_key)
if(param_disp!=null&&param_edit!=null){if(param_disp.unit!=ENUM_UNIT){RMCurrentUsualPopup(param_key,param_disp,param_edit);}
openEditParamPopup(param_disp.name);}else{var title=translate('remote_menu_param_edit_info')
if(param_disp!=null){title=param_disp.name;}
showAlertMessagePopup(translate('remote_menu_param_edit_lock'),title);}}