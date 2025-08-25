var alarms_tab=[];var remote_menu_alarmsnames=null
function clearServerAlarms(){$("#alarmsBtn").hide();var xx=$("#alarmsConfirm");xx.empty();xx.append($("<div>").ngt_prepare("ual_del_more"));xx.append($("<div>").append($("<button>").ngt_prepare("ui_btn_cancel").on("click",clearServerAlarmsCanc).addClass("ngstyle_button_large ngstyle_abort")).append($("<button>").ngt_prepare("ual_del_conf").on("click",clearServerAlarmsConf).addClass("ngstyle_button_large ngstyle_control")));}
function clearServerAlarmsCanc(){$("#alarmsConfirm").empty();$("#alarmsBtn").show();}
function clearServerAlarmsConf(){$("#alarmsConfirm").empty();$("#alarmsBtn").prop("disabled",true).show();jQuery.ajax("/service/deleteDeviceAlarms",{data:{uid:updater.currentDevice_},error:__clrAlmsERR,method:'POST',success:__clrAlmsOK,headers:{'X-CSRFToken':ngh_getcsrf()}});}
function __clrAlmsOK(){updateAlarmsCall();$("#alarmsBtn").prop("disabled",false);}
function __clrAlmsERR(){$("#alarmsBtn").prop("disabled",false);}
function alarmsResponse(in_alarms){alarms_tab=in_alarms;alarmsResponseRefresh();}
function alarmsResponseRefresh(){var alarms=alarms_tab;if(controller.protocol_type=='gm3'){return;}else{var table="<tr class='alarmsHeader'><th></th><th></th><th>"+translate("alarm")+"</th><th>"+translate("from")+"</th><th>"+translate("to")+"</th></tr>";var idx=0;if(remoteMenu&&remote_menu_alarmsnames!=null){for(a in alarms){++idx;table+="<tr class='"+(a%2==0?"one":"two")+"'><td class='tdAlarmsLp'>"+idx.toString()+
"</td><td class='tdAlarmsIcon'><i class='alarmRowIcon'></i></td><td class='tdAlarmsVal'><span>"+getAlarmName(alarms[a].code)+"</span></td><td class='tdAlarmsDate'>"+alarms[a].fromDate+
"</td><td class='tdAlarmsDate'>"+(alarms[a].toDate!=null?alarms[a].toDate:getAlarmName(255))+"</td></tr>";}}else{let alarms_currlang=trans_alarms[currLang];for(a in alarms){++idx;let alarmDesc="";if(controller.protocol_type=='gm3_pomp'){if(alarmsETtranslations!=null&&alarms[a].code in alarmsETtranslations){alarmDesc=getEtTranslationByLangNum(alarmsETtranslations[alarms[a].code]);let splitted=alarmDesc.split('|');if(splitted.length>3){var num=parseInt(splitted[1]);var unit=splitted[2];var conversion=parseInt(splitted[3]);var val=getCurrParamByNumber(num);if(val!=null){if(conversion in PARAM_TEXT_CONVERSIONS){val=PARAM_TEXT_CONVERSIONS[conversion](settings,val);}}else{val="";}
alarmDesc=splitted[0]+val+(unit in ETunits?ETunits[unit]:"");}}else{alarmDesc=translate("alarm")+" "+alarms[a].code;}}else{alarmDesc=undefined;if(alarms_currlang!==undefined){alarmDesc=alarms_currlang[alarms[a].code];}
if(alarmDesc===undefined){alarmDesc=trans_alarms["en"][alarms[a].code];}
if(alarmDesc===undefined){alarmDesc=translate("alarm")+" "+alarms[a].code;}}
table+="<tr class='"+(a%2==0?"one":"two")+"'><td class='tdAlarmsLp'>"+idx.toString()+
"</td><td class='tdAlarmsIcon'><i class='alarmRowIcon'></i></td><td class='tdAlarmsVal'><span>"+alarmDesc.split("\\n").join("<br>")+"</span></td><td class='tdAlarmsDate'>"+alarms[a].fromDate+
"</td><td class='tdAlarmsDate'>"+(alarms[a].toDate!=null?alarms[a].toDate:translate("alarmContinues"))+"</td></tr>";}}
$("#tabAlarms").empty();$("#tabAlarms").append(table);addTabToMenu("tabHrAlarms");}}
function getCurrParamByNumber(num){if(num in regParams){return regParams[num].val;}
return null;}
function getAlarmName(code){var codeStr=code.toString()
if(codeStr in remote_menu_alarmsnames){return remote_menu_alarmsnames[codeStr].replace("\\n",'<br>').replaceAll('\\n',' ');}
return"---"}
function getRemoteMenuAlarmsNamesResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&Object.keys(result.data).length>0){remote_menu_alarmsnames=result.data;updater.remoteMenuVer_[REMOTE_MENU_ALARMS_NAMES_]=(result.remoteMenuAlarmsNamesVer!=undefined)?result.remoteMenuAlarmsNamesVer:result.version;alarmsResponseRefresh();}else{remote_menu_alarmsnames=null;}}
function showEcoSolAlarms(alarms){if(alarms!=undefined){var table="<tr class='alarmsHeader'><th></th><th></th><th>"+translate("alarms")+"</th></tr>";var idx=0;for(var i=0;i<alarms.length;i+=1){if(alarms[i]=="1"){++idx;let alarmDesc=translate("EcosolAlarm"+i);table+="<tr class='"+(idx%2==0?"one":"two")+"'><td class='tdAlarmsLp'>"+idx.toString()+
"</td><td class='tdAlarmsIcon'><i class='alarmRowIcon'></i></td><td class='tdAlarmsVal'><span>"+alarmDesc+"</span></td></tr>";}}
if(idx>0){$("#tabAlarms").empty();$("#tabAlarms").append(table);addTabToMenu("tabHrAlarms");}
else{$("#tabAlarms").empty();$("#tabAlarms").append(table);removeTabFromMenu("tabHrAlarms");}}}
var schedulesData={};var originalSchedulesData={};var scheduleModes=[];var changingConstantValue=false;var currentConstantValue=null;var changedData=false;var changedHour=null;var savedSchedule=false;var decrMinVal=0;var decrMaxVal=0;var constBarWidth=24
var commonemBarWidth=0.4
var commongm3BarWidth=0.8
var ScheduleChartOptions={};var scheduleEcosolModes=["working_days","saturday","sunday"];function byteString(n){if(n<0||n>255||n%1!==0){throw new Error(n+" does not fit in a byte");}
return("000000000"+n.toString(2)).substr(-8)}
function drawScheduleChart(tab,placeholder,options,unit){if(!$("#"+placeholder).is('DIV')||tab.length==0){disableSchedule(placeholder);return;}
if(ScheduleChartOptions.commonem!=undefined){options.bars.barWidth=commonemBarWidth;}else if(ScheduleChartOptions.common!=undefined){options.bars.barWidth=commongm3BarWidth;}
drawSchedulePlot(tab,placeholder,options,unit);}
function drawConstant(value,placeholder,options,unit){if(!$("#scheduleChart").is('DIV')||value==null){disableSchedule("scheduleChart");return;}
options.bars.barWidth=constBarWidth;var tab=[];tab.push([24,value]);drawSchedulePlot(tab,"scheduleChart",options,unit);}
function drawSchedulePlot(tab,placeholder,options,unit){$('#schedulessErr').hide();$("#"+placeholder).show();$('#saveSchedulesBtn').prop('disabled',false);let safety=document.getElementById(placeholder);if((safety===null)||(safety.offsetWidth==0)||(safety.offsetHeight==0)){return;}
var plot=$.plot("#"+placeholder,[tab],options);$("#"+placeholder+" .xaxisLabel").css("top",$("#"+placeholder).height());}
function displayScheduleValErr(minv,maxv,value){var text=translate("data_bounds_err");text=text.replace("@minVal",minv);text=text.replace("@maxVal",maxv);if(isNaN(value)){text=translate("int_expected_err");}
var lbResult=document.getElementById('saveingEmSchedulesInfo');lbResult.className="errLabel";lbResult.innerHTML=text;}
function disableSchedule(placeholder){$('#schedulessErr').show();$('#saveSchedulesBtn').prop('disabled',true);$("#"+placeholder).hide();return;}
function updateSchedules(data){if(savedSchedule){savedSchedule=false;return;}
if(ngp_hide("schedules")){return;}
if(isScheduleTab()){if(!changedData){if(controller.protocol_type=="gm3"){$("#tabHrSchedules").show();updateSchedulesData(data);drawSchedule();}else if(controller.protocol_type=="em"){$("#tabHrEmSchedules").show();updateEmSchedulesData(data);initEmSchedules();drawEmSchedule();}}}
else{if(controller.protocol_type=="gm3_pomp"){if(jQuery.isEmptyObject(data)){return;};updateVentSchedulesData(data);$("#tabHrVentSchedules").show();}if(controller.protocol_type=="gm3"){updateSchedulesData(data);$("#tabHrSchedules").show();}else if(controller.protocol_type=="em"){$("#tabHrEmSchedules").show();updateEmSchedulesData(data);}}}
function isScheduleTab(){if(controller.only_device){for(const sdbm of document.getElementsByName("sidebar_menu")){if(!sdbm.checked){continue;}
return["tab_old_sched_gm","tab_old_sched_vent","tab_old_sched_em","tab_old_sched_tronic"].includes(sdbm.value);}}else{var currentTab=$(".current")[0];if((["tabHrSchedules","tabHrEmSchedules","tabHrETSchedules"]).indexOf(currentTab.id)>-1)
return true;return false;}}
function addHoverFunction(placeholder,param,mode,term){$("#"+placeholder).off("plothover");$("#"+placeholder).on("plothover",function(event,pos,item){if(item){var value=item.datapoint[1];$("#tooltip").remove();if(param in scheduleUnit){showTooltip(item.pageX+5,item.pageY+5,'#2f323b',"<p>"+value+" "+scheduleUnit[param]+"</p>");}else{showTooltip(item.pageX+5,item.pageY+5,'#2f323b',"<p>"+value+"</p>");}}else{$("#tooltip").remove();}
if(changedHour!=null&&mode!=null){schedulesData[param][mode][changedHour-1]=pos.y.toFixed();if(schedulesData[param][mode][changedHour-1]>ScheduleChartOptions[param].yaxis.max)
schedulesData[param][mode][changedHour-1]=ScheduleChartOptions[param].yaxis.max;if(schedulesData[param][mode][changedHour-1]<ScheduleChartOptions[param].yaxis.min)
schedulesData[param][mode][changedHour-1]=ScheduleChartOptions[param].yaxis.min;drawScheduleChart(prepareData(schedulesData,param,mode),"scheduleChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["common"]),scheduleUnit[param]);}
if(changingConstantValue){currentConstantValue=pos.y.toFixed();if(currentConstantValue>ScheduleChartOptions[param].yaxis.max)
currentConstantValue=ScheduleChartOptions[param].yaxis.max;if(currentConstantValue<ScheduleChartOptions[param].yaxis.min)
currentConstantValue=ScheduleChartOptions[param].yaxis.min;drawConstant(currentConstantValue,"scheduleChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["common"]),scheduleUnit[param]);}});}
function addClickFunction(placeholder,param,mode,therm){changedHour=null;changingConstantValue=false;$("#"+placeholder).off("plotclick");$("#"+placeholder).on("plotclick",function(event,pos,item){if(changedHour!==null||changingConstantValue==true){changedHour=null;changingConstantValue=false;return;}
if(pos.x>0&&pos.x<24&&pos.y>ScheduleChartOptions[param].yaxis.min&&pos.y<ScheduleChartOptions[param].yaxis.max){changedData=true;if(therm!=null&&mode!=null&&param==ecomaxScheduleParam){ClickFunctionForEcomaxSchedule(param,mode,pos.x,therm);}else if(mode!=null){ClickFunctionForSchedule(param,mode,pos.x);}
else{ClickFunctionForConstant(param,pos.y);}}
else{changedHour=null;changingConstantValue=false;}});}
function replaceAt(s,n,t){return s.substring(0,n)+t+s.substring(n+1);}
function MouseUpForSchedule(){changedHour=null;}
function MouseUpForConstant(){changingConstantValue=false;}
function showTooltip(x,y,color,contents,name){if(name==undefined){name="tooltip";}
$('<div id="'+name+'">'+contents+'</div>').css({position:'absolute',display:'none',top:y-80,left:x,border:'2px solid #ffffff',padding:'3px','font-size':'large','border-radius':'5px','color':'#ffffff','background-color':color}).appendTo("body").fadeIn(200);}
function saveSchedulesResponseMethod(result,textStatus,xmlhttprequest){if(result!=null){if(controller.protocol_type=="em"){var lbResult=document.getElementById('saveingEmSchedulesInfo');}else if(controller.protocol_type=="gm3"){var lbResult=document.getElementById('saveingSchedulesInfo');}else{var lbResult=document.getElementById('saveSchedulesETInfo');}
if(result.error!=null){lbResult.className="errLabel";lbResult.innerHTML=translate("error")+" "+translate(result.error);}
else{if(result.result=="OK"){lbResult.className="infoLabel";lbResult.innerHTML=translate("changes_saved");savedSchedule=true;}}
setTimeout(function(){lbResult.innerHTML=translate("");;},Parameters.HIDE_CONFIRM_DELAY);}}
function translateSchedules(){$("#pumpScheduleOption").text(translate("pump"));$("#scheduleModeLabel").text(translate($("#scheduleModeLabel").val()));$("#scheduleETModeLabel").text(translate(scheduleEcosolModes[$("#scheduleETModeLabel").attr("value")]));$('#scheduleChart .xaxisLabel').text(translate('hours'));$('#scheduleEmChart .xaxisLabel').text(translate('hours'));$('#scheduleETChart .xaxisLabel').text(translate('hours'));$("#saveSchedulesBtn").text(translate("save"));$("#saveEmSchedulesBtn").text(translate("save"));$("#scheduleEmModeLabel").text(translate($("#scheduleEmModeLabel").val()));$("#labelDecreaseVal").text(translate("labelDecreaseVal"));$("#scheduleChoice option").each(function(){$(this).text(translate($(this).val()));});$("#scheduleEmParam option").each(function(){$(this).text(translateScheduleOption($(this).val()));});$("#inpEditSchedOnOff option").each(function(){$(this).text(translate($(this).val()));});$("#scheduleETOnOff option").each(function(){$(this).text(translate($(this).val()));});$("#scheduleETParam option").each(function(){$(this).text(translate($(this).val()));});$(".scheduleOnOffFormater").each(function(){var prevWidth=$(this).width();$(this).text(translate($(this).attr("val")));var newLeft=parseInt($(this).parent().css("left"))+prevWidth-$(this).width();$(this).parent().css("left",newLeft)});}
function updateSchedulesCall(){controller.getSchedules(getSchedulesResponse);}
function getSchedulesResponse(result,textStatus,xmlhttprequest){if(checkCurrentDevActive()&&regAllowedAccess&&schedulesDataExists(result.schedules)&&!ngp_hide("schedules")){updateSchedules(result.schedules);updater.schedulesVer_=result.schedulesVer;}else{$("#tabHrSchedules").hide();$("#tabHrEmSchedules").hide();$("#tabHrETSchedules").hide();$("#tabHrVentSchedules").hide();}}
function schedulesDataExists(schedres){if(controller.protocol_type=="gm3_pomp"){return true;}
if(schedres!=undefined&&schedres!=null){var schkeys=Object.keys(schedres);if(schkeys.length>0){for(key in schkeys){var schedobj=schedres[schkeys[key]]
if(!$.isEmptyObject(schedobj)){return true;}}}}
return false;}
function addZeroToNumberString(number){if(number<10)
return"0"+number
return number}
function equalArrays(array1,array2){if(array1.length!=array2.length)return false;for(var i=0;i<array1.length;i++){if(array1[i]!=array2[i])return false;}
return true;}
var scheduleEcomaxModes=["sunday","monday","thuesday","wednesday","thursday","friday","saturday"];var ecomaxScheduleParam="ecomaxSchedules";var schedulesMap={"thermostat1TZ":"ecoSterTemp1","thermostat2TZ":"ecoSterTemp2","thermostat3TZ":"ecoSterTemp3","mixer1TZ":"mixerTemp1","mixer2TZ":"mixerTemp2","mixer3TZ":"mixerTemp3","mixer4TZ":"mixerTemp4","mixer5TZ":"mixerTemp5","mixer6TZ":"mixerTemp6","mixer7TZ":"mixerTemp7","mixer8TZ":"mixerTemp8","mixer9TZ":"mixerTemp9","mixer10TZ":"mixerTemp10","circuit1TZ":"mixerTemp1","circuit2TZ":"mixerTemp2","circuit3TZ":"mixerTemp3","circuit4TZ":"mixerTemp4","circuit5TZ":"mixerTemp5","circuit6TZ":"mixerTemp6","circuit7TZ":"mixerTemp7"}
var schedulesOrderArray=["boilerTZ","cwuTZ","circPumpTZ","boilerWorkTZ","boilerCleanTZ","exchangerCleanTZ","mixer1TZ","mixer2TZ","mixer3TZ","mixer4TZ","mixer5TZ","mixer6TZ","mixer7TZ","mixer8TZ","mixer9TZ","mixer10TZ","thermostat1TZ","thermostat2TZ","thermostat3TZ","circuit1TZ","circuit2TZ","circuit3TZ","circuit4TZ","circuit5TZ","circuit6TZ","circuit7TZ",'panel1TZ','panel2TZ','panel3TZ','panel4TZ','panel5TZ','panel6TZ','panel7TZ','mainHeSoTZ','heatCirc','embeddedThermo','heater','cwu2TZ','intake','intakeSummer'];var noDecrSchedulesTable=["circPumpTZ","boilerWorkTZ","boilerCleanTZ","exchangerCleanTZ","embeddedThermo"]
function prepareDataEcomaxSchedule(data,param,mode,term){var tab=[];if(data[param]!=undefined&&data[param][term]!=undefined&&data[param][term].length>0){dayData=data[param][term][scheduleModes.indexOf(mode)]
infoData=data[param][term][scheduleModes.length]
if(infoData!=undefined){if(infoData.length==4){$("#inpEditSchedOnOff").val(infoData[0]);$("#inpEditSchedDecreaseValue").val(infoData[1]);decrMinVal=infoData[2];decrMaxVal=infoData[3];if(decrMinVal==decrMaxVal){$('#labelDecreaseVal').hide();$('#inpEditSchedDecreaseValue').hide();$('#inpEditSchedOnOffDiv').hide();}else if(decrMinVal>decrMaxVal){$('#labelDecreaseVal').hide();$('#inpEditSchedDecreaseValue').hide();$('#inpEditSchedOnOffDiv').show();}else{$('#labelDecreaseVal').show();$('#inpEditSchedDecreaseValue').show();$('#inpEditSchedOnOffDiv').show();}
if(noDecrSchedulesTable.indexOf(term)!=-1){$('#labelDecreaseVal').hide();$('#inpEditSchedDecreaseValue').hide();}
$('#inpEditSchedOnOff').selectric('refresh');}}
for(var i=0;i<dayData.length;i++){var tmpString=byteString(dayData[i])
for(var j=0;j<tmpString.length;j++){tab.push([(j+(i*tmpString.length))*0.5+0.05,tmpString[j]]);}}}
return tab;}
function drawEmSchedule(){resizeEmArea();$("#schedulesEmSchedParams").show();scheduleModes=scheduleEcomaxModes;$("#scheduleEmMode").show();if($("#scheduleEmModeLabel").val()==''){$("#scheduleEmModeLabel").val(scheduleModes[0]);}
var mode=$("#scheduleEmModeLabel").val();$("#scheduleEmModeLabel").text(translate(mode));if(originalSchedulesData==undefined){return;}
schedulesData=jQuery.extend(true,{},originalSchedulesData);drawScheduleChart(prepareDataEcomaxSchedule(originalSchedulesData,ecomaxScheduleParam,mode,$("#scheduleEmParam").val()),"scheduleEmChart",$.extend({},ScheduleChartOptions[ecomaxScheduleParam],ScheduleChartOptions["commonem"]),"");addClickFunction("scheduleEmChart",ecomaxScheduleParam,mode,$("#scheduleEmParam").val());}
function showEmNextMode(){var modeNo=scheduleModes.indexOf($("#scheduleEmModeLabel").val());updateEmScheduleMode(modeNo+1);}
function showEmPrevMode(){var modeNo=scheduleModes.indexOf($("#scheduleEmModeLabel").val());if(modeNo==0){modeNo=scheduleModes.length;}
updateEmScheduleMode(modeNo-1);}
function updateEmScheduleMode(modeNo){modeNo=modeNo%scheduleModes.length;$("#scheduleEmModeLabel").val(scheduleModes[modeNo]);drawEmSchedule();}
function updateEmSchedulesData(data){for(var param in data){schedulesData[param]={};for(var mode in data[param]){if(data[param][mode].length!=0){schedulesData[param][mode]=data[param][mode];}}}
originalSchedulesData=jQuery.extend(true,{},schedulesData);}
function ClickFunctionForEcomaxSchedule(param,mode,posx,therm){changedHour=Math.floor(posx*2);var dayScheduleData=schedulesData[param][therm][scheduleModes.indexOf(mode)];for(var i=0;i<dayScheduleData.length;i++){if(changedHour<((i*8)+8)){var partStr=byteString(dayScheduleData[i])
var ind=changedHour-(i*8);if(partStr[ind]=="1"){partStr=replaceAt(partStr,ind,'0');}else{partStr=replaceAt(partStr,ind,'1');}
dayScheduleData[i]=parseInt(partStr,2);break;}}
changedHour=null;drawScheduleChart(prepareDataEcomaxSchedule(schedulesData,param,mode,therm),"scheduleEmChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["commonem"]),"");}
function saveEmSchedules(){var dval=$("#inpEditSchedDecreaseValue").val()
if(((decrMinVal!=decrMaxVal)&&(decrMinVal<decrMaxVal)&&((dval<decrMinVal)||(dval>decrMaxVal)))||isNaN(dval)){displayScheduleValErr(decrMinVal,decrMaxVal,dval);}else{var mode=$("#scheduleEmModeLabel").val();var scheduleParams=schedulesData[ecomaxScheduleParam][$("#scheduleEmParam").val()][scheduleModes.length];scheduleParams[0]=$("#inpEditSchedOnOff").val();scheduleParams[1]=dval;controller.saveSchedules(ecomaxScheduleParam,scheduleModes.indexOf(mode),schedulesData[ecomaxScheduleParam][$("#scheduleEmParam").val()],saveSchedulesResponseMethod,$("#scheduleEmParam").val());originalSchedulesData=jQuery.extend(true,{},schedulesData);changedData=false;}}
function initEmSchedulesArea(){initEmSchedules();drawEmSchedule();}
function resizeEmArea(){$("#scheduleEmChart").width($('#schedulesEmMain').width()/1.05);$("#scheduleEmChart").height($("#scheduleEmChart").width()/3);}
function initEmSchedules(){clearDict(ScheduleChartOptions);ScheduleChartOptions["commonem"]={series:{points:{show:false},bars:{show:true,},color:'#000000',},bars:{align:"left",barWidth:0.4,borderWidth:0,lineWidth:0,fill:true,fillColor:{colors:['#03d4ee','#48759c']},},xaxis:{min:0,max:24,tickSize:1,tickDecimals:0,tickLength:0,borderWidth:3,tickColor:'#acacac'},grid:{hoverable:true,clickable:true,backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:0,bottom:2,right:0},labelMargin:15},yaxis:{min:-0.03,max:1,tickSize:1,tickLength:0,ticks:[[0,""],[1,""]],tickColor:'#acacac'}};ScheduleChartOptions["ecosterThermostats"]={yaxis:{min:0,max:1,tickSize:1,tickDecimals:0}};ScheduleChartOptions["ecomaxSchedules"]={yaxis:{min:0,max:1,ticks:[[1,""]],tickSize:1,tickDecimals:0}};var ecomaxSchedKeys=Object.keys(originalSchedulesData[ecomaxScheduleParam]);if(ecomaxSchedKeys!=undefined){var arr=[];if(tiles_dict!='undefined'){for(var i=0;i<ecomaxSchedKeys.length;i++){if(ecomaxSchedKeys[i]in schedulesMap&&controller.type_!=ECOMAX_850i_TYPE){if(schedulesMap[ecomaxSchedKeys[i]]in tiles_dict){arr.push(addZeroToNumberString(schedulesOrderArray.indexOf(ecomaxSchedKeys[i]))+"_"+ecomaxSchedKeys[i]);}}else{arr.push(addZeroToNumberString(schedulesOrderArray.indexOf(ecomaxSchedKeys[i]))+"_"+ecomaxSchedKeys[i]);}}}
if(($("#scheduleEmParam").children().length==0)||($("#scheduleEmParam").children().length!=arr.length)){arr.sort();$("#scheduleEmParam").children().remove();for(var i=0;i<arr.length;i++){var kvalue=arr[i].split('_')[1];$("#scheduleEmParam").append($("<option>").attr("value",kvalue).text(kvalue));}}
$("#scheduleEmParam option").each(function(){$(this).text(translateScheduleOption($(this).val()));});$("#inpEditSchedOnOff option").each(function(){$(this).text(translate($(this).val()));});}
$('#inpEditSchedOnOff').selectric('refresh');$('#scheduleEmParam').selectric('refresh');}
var scheduleUnit={"TCWUmin":'°C',"Cyrkulacja":""}
function prepareData(data,param,mode){var tab=[];if(data[param]!=undefined&&data[param][mode]!=undefined&&data[param][mode].length>0){for(var i=0;i<24;i++){tab.push([i+0.9,data[param][mode][i]]);}}
return tab;}
function drawSchedule(){resizeArea();var param=$("#scheduleParam").val();changedData=false;if($("#scheduleChoice").val()=="schedule"){$("#scheduleMode").show();if($("#scheduleModeLabel").val()==''){$("#scheduleModeLabel").val(scheduleModes[0]);}
var mode=$("#scheduleModeLabel").val();$("#scheduleModeLabel").text(translate(mode));if(originalSchedulesData==undefined){return;}
schedulesData=jQuery.extend(true,{},originalSchedulesData);drawScheduleChart(prepareData(originalSchedulesData,param,mode),"scheduleChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["common"]),scheduleUnit[param]);addHoverFunction("scheduleChart",param,mode);addClickFunction("scheduleChart",param,mode);}else{$("#scheduleMode").hide();currentConstantValue=parameters_current[param].value;drawConstant(currentConstantValue,"scheduleChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["common"]),scheduleUnit[param]);addHoverFunction("scheduleChart",param);addClickFunction("scheduleChart",param);}}
function showNextMode(){var modeNo=scheduleModes.indexOf($("#scheduleModeLabel").val());updateScheduleMode(modeNo+1);}
function showPrevMode(){var modeNo=scheduleModes.indexOf($("#scheduleModeLabel").val());if(modeNo==0){modeNo=scheduleModes.length;}
updateScheduleMode(modeNo-1);}
function updateScheduleMode(modeNo){modeNo=modeNo%scheduleModes.length;$("#scheduleModeLabel").val(scheduleModes[modeNo]);drawSchedule();}
function updateSchedulesData(data){if((jQuery.isEmptyObject(data))||(ngp_hide("schedules"))){$("#tabHrSchedules").hide();}
else{for(var param in data){for(var mode in data[param]){if(data[param][mode].length!=0){if(schedulesData[param]==undefined)schedulesData[param]={};schedulesData[param][mode]=data[param][mode];}}}
$("#tabHrSchedules").show();originalSchedulesData=jQuery.extend(true,{},schedulesData);}}
function saveSchedules(){var param=$("#scheduleParam").val();var mode=$("#scheduleModeLabel").val();if($("#scheduleChoice").val().indexOf("ecosterThermSchedule")>=0&&schedulesData[param]!=undefined){controller.saveSchedules(param,scheduleModes.indexOf(mode),schedulesData[param][$("#scheduleChoice").val()],saveSchedulesResponseMethod,$("#scheduleChoice").val());originalSchedulesData=jQuery.extend(true,{},schedulesData);}else if($("#scheduleChoice").val()=="schedule"&&schedulesData[param]!=undefined&&schedulesData[param][mode]!=undefined){controller.saveSchedules(param,mode,schedulesData[param][mode],saveSchedulesResponseMethod);originalSchedulesData=jQuery.extend(true,{},schedulesData);if(param=="Cyrkulacja")
{controller.saveParam(parameters_current[param].num,0,saveSchedulesResponseMethod);controller.saveParam(parameters_current["Cyrkulacjaharm"].num,1,saveSchedulesResponseMethod);}
else if(param=="TCWUmin")
{controller.saveParam(parameters_current["TCWUminharm"].num,1,saveSchedulesResponseMethod);}}
else if(param=="Cyrkulacja"&&$("#scheduleChoice").val()=="constant"&&currentConstantValue!=null)
{controller.saveParam(parameters_current[param].num,currentConstantValue,saveSchedulesResponseMethod);controller.saveParam(parameters_current["Cyrkulacjaharm"].num,0,saveSchedulesResponseMethod);}
else if(param=="TCWUmin"&&$("#scheduleChoice").val()=="constant"&&currentConstantValue!=null)
{controller.saveParam(parameters_current[param].num,currentConstantValue,saveSchedulesResponseMethod);controller.saveParam(parameters_current["TCWUminharm"].num,0,saveSchedulesResponseMethod);}
else{if($("#scheduleChoice").val()=="constant"&&currentConstantValue!=null&&!changingConstantValue){controller.saveParam(parameters_current[param].num,currentConstantValue,saveSchedulesResponseMethod);}}
changedData=false;}
function ClickFunctionForSchedule(param,mode,posx){changedHour=Math.ceil(posx);if(param=="Cyrkulacja"){schedulesData[param][mode][changedHour-1]=!schedulesData[param][mode][changedHour-1];changedHour=null;drawScheduleChart(prepareData(schedulesData,param,mode),"scheduleChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["common"]),scheduleUnit[param]);}}
function ClickFunctionForConstant(param,posy){changingConstantValue=true;if(param=="Cyrkulacja"){currentConstantValue=!currentConstantValue;changingConstantValue=false;drawConstant(Number(currentConstantValue),"scheduleChart",$.extend({},ScheduleChartOptions[param],ScheduleChartOptions["common"]),scheduleUnit[param]);}}
function initGmSchedules(){initSchedules();drawSchedule();}
function resizeArea(){$("#scheduleChart").width($('#schedulesMain').width()/1.05);$("#scheduleChart").height($("#scheduleChart").width()/3);}
function initSchedules(){clearDict(ScheduleChartOptions);ScheduleChartOptions["common"]={series:{points:{show:false},bars:{show:true,},color:'#000000'},bars:{show:true,barWidth:0.8,borderWidth:0,lineWidth:0,fill:true,fillColor:{colors:['#03d4ee','#48759c']},align:"right",},xaxis:{min:0,max:24,tickSize:1,tickDecimals:0,tickLength:0,},};ScheduleChartOptions["Cyrkulacja"]={yaxis:{min:-0.03,max:1,tickSize:1,tickLength:0,tickDecimals:0},grid:{hoverable:true,clickable:true,backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:0,bottom:2,right:0},labelMargin:15}};if("Nazwa"in parameters_current&&parameters_current["Nazwa"]["value"]=="ecoSOL 301"&&"logoNum"in schema&&schema.logoNum==131){ScheduleChartOptions["TCWUmin"]={yaxis:{min:5,max:80,tickLength:10,},grid:{hoverable:true,clickable:true,backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:2,bottom:2,right:0},labelMargin:15}};}else{ScheduleChartOptions["TCWUmin"]={yaxis:{min:20,max:80,tickLength:10,},grid:{hoverable:true,clickable:true,backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:2,bottom:2,right:0},labelMargin:15}};}
scheduleModes=scheduleEcosolModes;var schedule=$("#scheduleParam").val()+"harm";if(parameters_current[schedule]!=undefined){if(parameters_current[schedule].value){$("#scheduleChoice").val("schedule");}
else{$("#scheduleChoice").val("constant");}
$('#scheduleChoice').selectric('refresh');}}
var scheduleETModes=["W","Sa","Su"];scheduleETParams={"CWU":["CWUSETT",4,1],"CWUC":["CWUSETT",32,1],"M1":["M1SETT",16,4],"M2":["M2SETT",16,4],"M3":["M3SETT",16,4],"H1":["H1SETT",1048576,1],"H2":["H2SETT",1048576,1],"LP":["LPSETT",4194304,1],};var currRanges={1:[],2:[],3:[]};var newRanges={1:[],2:[],3:[]};var currScheduleETParam=null;var changingScheduleStart=false;var changingScheduleStop=false;var changingScheduleValue=false;var changingScheduleRange=0;var changingScheduleRange=0;var changingScheduleET=false;var changingScheduleETEnd=false;var changingScheduleIndex=null;var tempSchedules=false;var drawingSingleChart=false;var ETplot;var isDrawingToLeft=false;var isDrawingToRight=false;var startingPoint;var locationItems=[];var drawingLeft='left';var drawingRight='right';var drawingCenter='center';var schedulesIndexes={};var ScheduleChartETOptions={series:{points:{show:false},bars:{show:true,},color:'#2f323b',},bars:{show:true,lineWidth:0.8,fill:true,fillColor:{colors:['#03d4ee','#48759c']},align:"right",},xaxis:{min:0,max:24,tickSize:1,tickFormatter:hourFormatter,tickDecimals:0,rotateTicks:90},yaxis:{min:0,max:21,tickSize:1,tickDecimals:0,tickFormatter:onoffFormatter,},grid:{hoverable:true,clickable:true,backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:2,bottom:2,right:0},labelMargin:15},canvas:false,}
function onoffFormatter(v,axis){var value=v?'off':'on';return'<label class="scheduleOnOffFormater" val="'+value+'">'+translate(value)+'</label>';}
function hourFormatter(v,axis){return v+":00";}
function initETSchedules(){$("#scheduleETModeLabel").val(0);$("#scheduleETModeLabel").text(translate(scheduleEcosolModes[0]));$("#"+"scheduleETChart").bind("plotmouseup",function(event,pos,item){changingScheduleStart=false;changingScheduleStop=false;changingScheduleValue=false;setTimeout(function(){changingScheduleET=false;},60000);});addScheduleClickET("scheduleETChart");addScheduleHoverET("scheduleETChart");}
function updateScheduleModeET(dif){var modeNo=parseInt($("#scheduleETModeLabel").attr("value"));if(modeNo==0){modeNo=scheduleETModes.length;}
modeNo=(modeNo+dif)%scheduleETModes.length;$("#scheduleETModeLabel").attr("value",modeNo);$("#scheduleETModeLabel").text(translate(scheduleEcosolModes[modeNo]));drawETSchedule();}
function updateETSchedule(){setAvailableSchedules();if(isScheduleTab()&&!changingScheduleET){drawETSchedule();}}
function saveSchedulesET(){var mode=scheduleETModes[$("#scheduleETModeLabel").attr("value")];saveScheduleET(currScheduleETParam,mode,1);saveScheduleET(currScheduleETParam,mode,2);saveScheduleET(currScheduleETParam,mode,3);if(tempSchedules){var val=(getU2number(-newRanges[3][2])<<16)+(getU2number(-newRanges[2][2])<<8)+(getU2number(-newRanges[1][2]))
controller.saveParam(regParams[currScheduleETParam+"_TZ"+mode+"T"].num,val,saveSchedulesResponseMethod);}
turnOnOffETSchedule(currScheduleETParam);changingScheduleET=false;}
function getU2number(val){if(val<0){val=256+val;}
return val;}
function saveScheduleET(param,mode,num){if((newRanges[num]).length>2){var val=((newRanges[num][1][1])<<24)+((newRanges[num][1][0])<<16)+(newRanges[num][0][1]<<8)+(newRanges[num][0][0]);controller.saveParam(regParams[param+"_TZ"+mode+num].num,val,saveSchedulesResponseMethod);}}
function resizeEtArea(){$("#scheduleETChart").width($('#schedulesETMain').width()/1.1);$("#scheduleETChart").height($("#scheduleETChart").width()/3);}
function drawETSchedule(resizing){changingScheduleStart=false;changingScheduleStop=false;changingScheduleET=false;var mode=scheduleETModes[$("#scheduleETModeLabel").attr("value")];currScheduleETParam=$("#scheduleETParam").val();$("#scheduleETOnOff").val((scheduleOn(currScheduleETParam)).toString()).selectric('refresh');currRanges[1]=getRangeHours(currScheduleETParam,mode,1);currRanges[2]=getRangeHours(currScheduleETParam,mode,2);currRanges[3]=getRangeHours(currScheduleETParam,mode,3);addValuesToRanges(currScheduleETParam,mode,currRanges);if(!rangesEqual(currRanges,newRanges)||(resizing!=undefined&&resizing)){newRanges=$.extend(true,{},currRanges);plotETSchedule(newRanges,"scheduleETChart");}}
function rangesEqual(first,second){for(var i in first){if(first[i].length!=second[i].length){return false;}
for(var j=0;j<2;j++){for(var k=0;k<2;k++){if(second[i][j][k]!=first[i][j][k]){return false;}}}
if(first[i][2]!=second[i][2]){return false;}}
return true;}
function getRangeHours(param,mode,num){return prepareETData(getRegParamIfExists(param+"_TZ"+mode+num).val);}
function addValuesToRanges(param,mode,ranges){var val=getRegParamIfExists(param+"_TZ"+mode+"T").val;if(val!=null){tempSchedules=true;ranges[1].push(-(-(val&0x80)+(val&0x7f)));val=val>>8;ranges[2].push(-(-(val&0x80)+(val&0x7f)));val=val>>8;ranges[3].push(-(-(val&0x80)+(val&0x7f)));}
else{tempSchedules=false;ranges[1].push(1);ranges[2].push(1);ranges[3].push(1);}}
function plotETSchedule(ranges,placeholder){resizeEtArea();if(tempSchedules){ScheduleChartETOptions.yaxis.max=21;ScheduleChartETOptions.yaxis.tickFormatter=undefined;}
else{ScheduleChartETOptions.yaxis.max=1;ScheduleChartETOptions.yaxis.tickFormatter=onoffFormatter;}
var tab=[];schedulesIndexes={};addRangeToChart(tab,1,ranges);addRangeToChart(tab,2,ranges);addRangeToChart(tab,3,ranges);$("#"+placeholder).empty();let safety=document.getElementById(placeholder);if((safety===null)||(safety.offsetWidth==0)||(safety.offsetHeight==0)){return;}
ETplot=$.plot("#"+placeholder,tab,ScheduleChartETOptions);var xaxisLabel=$("<div class='axisLabel xaxisLabel'></div>").text(translate('hours')).appendTo("#"+placeholder);$("#"+placeholder+" .xaxisLabel").css("top",$("#"+placeholder).height());}
function addRangeToChart(tab,num,ranges){var start=tabHourToFloat(ranges[num][0]);var stop=tabHourToFloat(ranges[num][1])
if(start<=stop){tab.push({data:[[stop,ranges[num][2]]],bars:{barWidth:stop-start},});schedulesIndexes[Object.keys(schedulesIndexes).length]=num;}
else{tab.push({data:[[24,ranges[num][2]]],bars:{barWidth:24-start},});tab.push({data:[[stop,ranges[num][2]]],bars:{barWidth:stop},});schedulesIndexes[Object.keys(schedulesIndexes).length]=num;schedulesIndexes[Object.keys(schedulesIndexes).length]=num;}}
function tabHourToFloat(tab){return tab[0]+tab[1]/60;}
function floatTotabHour(val){return[parseInt(val),(val%1)*60];}
function setEndPosition(item,pos)
{var posLeft=parseFloat(item[0][0]+'.'+item[0][1]).toFixed(2);var posRight=parseFloat(item[1][0]+'.'+item[1][1]).toFixed(2);if(posLeft==startingPoint)
item[1]=getRangeVal(pos.x);else if(posRight==startingPoint)
item[0]=getRangeVal(pos.x);changeRangeVal(pos.y);}
function finishDrawing(placeholder)
{drawingSingleChart=false;$("#tooltipStart").remove();$("#tooltipEnd").remove();$("#tooltipVal").remove();}
function setStartingPointForExistingItem(item,posX)
{var posLeft=parseFloat(item[0][0]+'.'+item[0][1]).toFixed(2);var posRight=parseFloat(item[1][0]+'.'+item[1][1]).toFixed(2);var middlePoint=parseFloat(posLeft)+(parseFloat(posRight)-parseFloat(posLeft))/2;if(middlePoint>posX)
startingPoint=posRight;else
startingPoint=posLeft;}
function beginEditExistingItem(item,pos)
{changingScheduleIndex=schedulesIndexes[item.seriesIndex];var start=tabHourToFloat(newRanges[changingScheduleIndex][0]);var end=tabHourToFloat(newRanges[changingScheduleIndex][1]);if(end==0&&start!=0){end=24;}
var changingItem=newRanges[changingScheduleIndex];setStartingPointForExistingItem(changingItem,pos.x);}
function endItemEdition(pos)
{var changingItem=newRanges[changingScheduleIndex];setEndPosition(changingItem,pos);setDrawingCenter();}
function createNewElement(pos)
{changingScheduleIndex=getFreeItemIndex();if(changingScheduleIndex==-1)
{finishDrawing(placeholder);return;}
setDrawingCenter();changeStartRangeVal(pos.x,pos.y);startingPoint=pos.x.toFixed(2);}
function addScheduleClickET(placeholder){var placeholderItem=$("#"+placeholder);placeholderItem.off("plotclick");placeholderItem.on("plotclick",function(event,pos,item){if(pos.x>=0&&pos.x<24&&pos.y>ScheduleChartETOptions.yaxis.min&&pos.y<=ScheduleChartETOptions.yaxis.max)
{if(!drawingSingleChart)
{addScheduleHoverET(placeholder);drawingSingleChart=true;changingScheduleET=true;}
else
finishDrawing(placeholder);if(item)
beginEditExistingItem(item,pos);else if(!drawingSingleChart)
endItemEdition(pos);else
createNewElement(pos);}
else if(pos.x>=0&&pos.x<24&&pos.y>=ScheduleChartETOptions.yaxis.min-10&&changingScheduleIndex!=null&&changingScheduleIndex>0)
{var changingItem=newRanges[changingScheduleIndex];changingItem[0]=getRangeVal(0);changingItem[1]=getRangeVal(0);changingItem[2]=0;finishDrawing(placeholder);plotETSchedule(newRanges,placeholder);}});}
function changeStartRangeVal(posx,posy){newRanges[changingScheduleIndex][0]=getRangeVal(posx);newRanges[changingScheduleIndex][2]=Math.max(0,Math.min(parseInt(posy),ScheduleChartETOptions.yaxis.max));}
function getRangeVal(posx){return floatTotabHour(Math.min(24,Math.max(posx,0)));}
function changeRangeVal(posy){newRanges[changingScheduleIndex][2]=Math.max(0,Math.min(parseInt(posy),ScheduleChartETOptions.yaxis.max));}
function getFreeItemIndex()
{var tempEmptyPoint=[0,0].toString();for(i=1;i<4;i++)
{if(newRanges[i][1].toString()==tempEmptyPoint)
return i;}
return-1;}
function findNearestRange(posx){var num=1;var minDist=distPositionRange(posx,num);for(var i in newRanges){var dist=distPositionRange(posx,i);if(dist<minDist){minDist=dist;num=i;}}
return num;}
function distPositionRange(posx,rangeNum){return Math.abs((tabHourToFloat(newRanges[rangeNum][0])+tabHourToFloat(newRanges[rangeNum][1]))/2-posx);}
function setDrawingToLeft()
{isDrawingToLeft=true;isDrawingToRight=false;}
function setDrawingToRight()
{isDrawingToLeft=false;isDrawingToRight=true;}
function setDrawingCenter()
{isDrawingToLeft=false;isDrawingToRight=false;}
function getDrawingDirection(item,posX)
{var posLeft=parseFloat(item[0][0]+'.'+item[0][1]).toFixed(2);var posRight=parseFloat(item[1][0]+'.'+item[1][1]).toFixed(2);if(posX>startingPoint)
return drawingRight;else if(posX<startingPoint)
return drawingLeft;else
return drawingCenter;}
function getPixelFactor()
{var plotWidth=Math.abs(locationItems[0][0]-locationItems[1][0]);var pixelAmount=Math.abs(locationItems[0][1]-locationItems[1][1]);var pixelFactor=pixelAmount/plotWidth;return pixelFactor;}
function drawTooltip(pos,changingItem)
{var pixelFactor=getPixelFactor();var changingItemWidth=Math.abs(tabHourToFloat(changingItem[0])-tabHourToFloat(changingItem[1]));var leftTooltipPosX=pos.pageX-changingItemWidth*pixelFactor-65;var rightTooltipPosition=pos.pageX+15+changingItemWidth*pixelFactor;var centerTooltipPosX=pos.pageX-5+(changingItemWidth*pixelFactor)/2;if(isDrawingToRight)
{rightTooltipPosition=pos.pageX+15;centerTooltipPosX=pos.pageX-5-(changingItemWidth*pixelFactor)/2}
if(isDrawingToLeft)
leftTooltipPosX=pos.pageX-65;plotAxes=ETplot.getAxes();$("#tooltipStart").remove();$("#tooltipEnd").remove();$("#tooltipVal").remove();showTooltip(leftTooltipPosX,pos.pageY+60,'#2f323b',"<p>"+changingItem[0][0]+":"+parseInt(changingItem[0][1])+"</p>","tooltipStart");showTooltip(rightTooltipPosition,pos.pageY+60,'#2f323b',"<p>"+changingItem[1][0]+":"+parseInt(changingItem[1][1])+"</p>","tooltipEnd");showTooltip(centerTooltipPosX,pos.pageY,'#2f323b',"<p>"+changingItem[2]+"</p>","tooltipVal");}
function addScheduleHoverET(placeholder){$("#"+placeholder).off("plothover");$("#"+placeholder).on("plothover",function(event,pos,item){plotAxes=ETplot.getAxes();if(!drawingSingleChart||pos.y>=plotAxes.yaxis.max||pos.y<0)
return;if(locationItems.length<2)
{if(locationItems.length==1&&pos.x<locationItems[0][0]-2&&pos.x>locationItems[0][0]+2)
return;locationItems.push([pos.x,pos.pageX]);return;}
var changingItem=newRanges[changingScheduleIndex];drawTooltip(pos,changingItem);var drawingDirection=getDrawingDirection(changingItem,pos.x);if(drawingDirection==drawingLeft)
{changingItem[1]=getRangeVal(startingPoint);changingItem[0]=getRangeVal(pos.x);setDrawingToLeft();}
else if(drawingDirection==drawingRight)
{changingItem[1]=getRangeVal(pos.x);changingItem[0]=getRangeVal(startingPoint);setDrawingToRight();}
else if(drawingDirection==drawingCenter)
{setDrawingCenter();}
if(!tempSchedules&&pos.y>0.5)
pos.y=1;changeRangeVal(pos.y);plotETSchedule(newRanges,placeholder);});}
function prepareETData(val){var start=[(val&0xff),((val>>8)&0xff)];var stop=[((val>>16)&0xff),((val>>24)&0xff)];return[start,stop];}
function setAvailableSchedules(){$("#scheduleETParam").empty();for(var i in scheduleETParams){if(!(i[0]=="H"&&$("#scheduleETParam option[value='M"+i[1]+"']").length>0)){var sett=getRegParamIfExists(scheduleETParams[i][0]).val;if(sett!=null&&sett&scheduleETParams[i][2]){$("#scheduleETParam").append('<option value="'+i+'">'+translate(i)+'</option>');}}}
if(ngp_hide("schedules")||$("#scheduleETParam option").length==0){$("#tabHrETSchedules").hide();}else{$("#tabHrETSchedules").show();if(currScheduleETParam){$("#scheduleETParam").val(currScheduleETParam);}
else{currScheduleETParam=$("#scheduleETParam").val();}
addTabToMenu("tabHrETSchedules");}
$('#scheduleETParam').selectric('refresh');}
function turnOnOffETSchedule(param){var paramSet=scheduleETParams[param][0];var val=getRegParamIfExists(paramSet).val;if(val!=null){if(parseInt($("#scheduleETOnOff").val())){val=val|scheduleETParams[param][1];}
else{val=val&(~scheduleETParams[param][1])}
controller.saveParam(regParams[paramSet].num,val,saveSchedulesResponseMethod);}}
function scheduleOn(param){var paramSet=scheduleETParams[param][0];var val=getRegParamIfExists(paramSet).val;val=val&scheduleETParams[param][1];if(val==scheduleETParams[param][1]){return 1;}
return 0;}
var scheduleVentModes=["monday","thuesday","wednesday","thursday","friday","saturday","sunday"];var ventSchedulesData=[];var ventSchedulesFlotData=[[],[],[],[],[],[],[]];var ranges=[];var weeklyRanges=[[],[],[],[],[],[],[],[]];var deleteMode=false;var dots=0;var saveSchedulesInterval;var offVentSchedule;var offVentScheduleName;var offVentScheduleNum;var seriesForHover=[[0,1],[0.5,1],[1,1],[1.5,1],[2,1],[2.5,1],[3,1],[3.5,1],[4,1],[4.5,1],[5,1],[5.5,1],[6,1],[6.5,1],[7,1],[7.5,1],[8,1],[8.5,1],[9,1],[9.5,1],[10,1],[10.5,1],[11,1],[11.5,1],[12,1],[12.5,1],[13,1],[13.5,1],[14,1],[14.5,1],[15,1],[15.5,1],[16,1],[16.5,1],[17,1],[17.5,1],[18,1],[18.5,1],[19,1],[19.5,1],[20,1],[20.5,1],[21,1],[21.5,1],[22,1],[22.5,1],[23,1],[23.5,1]];var ScheduleChartVENTOptions={xaxis:{tickLength:0,min:-0.1,max:24,tickSize:1,ticks:[[0,'0'],[1,'1'],[2,'2'],[3,'3'],[4,'4'],[5,'5'],[6,'6'],[7,'7'],[8,'8'],[9,'9'],[10,'10'],[11,'11'],[12,'12'],[13,'13'],[14,'14'],[15,'15'],[16,'16'],[17,'17'],[18,'18'],[19,'19'],[20,'20'],[21,'21'],[22,'22'],[23,'23'],[24,'24']],tickColor:'#acacac'},grid:{hoverable:true,clickable:true,backgroundColor:null,borderColor:'#acacac',borderWidth:{top:0,left:0,bottom:2,right:0},labelMargin:15,},yaxis:{tickLength:0,ticks:[],min:-0.03,max:1},selection:{mode:'x',minSize:0,min:10,max:20,},};function setVentSchedulesFlotDataDefault(){for(var i=0;i<7;i++){for(var j=0;j<5;j++){var emptySeries=[[0,0],[0.5,0],[1,0],[1.5,0],[2,0],[2.5,0],[3,0],[3.5,0],[4,0],[4.5,0],[5,0],[5.5,0],[6,0],[6.5,0],[7,0],[7.5,0],[8,0],[8.5,0],[9,0],[9.5,0],[10,0],[10.5,0],[11,0],[11.5,0],[12,0],[12.5,0],[13,0],[13.5,0],[14,0],[14.5,0],[15,0],[15.5,0],[16,0],[16.5,0],[17,0],[17.5,0],[18,0],[18.5,0],[19,0],[19.5,0],[20,0],[20.5,0],[21,0],[21.5,0],[22,0],[22.5,0],[23,0],[23.5,0]];ventSchedulesFlotData[i][j]=emptySeries;};};};function updateVentSchedulesData(data){if(data=='{}'){return;};var params=JSON.parse(data);if(checkVentScheduleFlag==true){var ver=params.ver;var lastSchedule=JSON.parse(localStorage.getItem('lastScheduleVent'));var tmpParams=params.values[0];for(var i=0;i<tmpParams.length;i++){for(var j=0;j<tmpParams[i].length;j++){if(tmpParams[i][j][0][0]==-1){tmpParams[i][j][2]=-1;};};};if(lastSchedule.value==JSON.stringify(tmpParams)){checkVentScheduleFlag=false;unlockVentButtons();clearInterval(saveSchedulesInterval);$("#saveSchedulesVENTInfSucces").attr("hidden",false);setTimeout(function(){$("#saveSchedulesVENTInfSucces").attr("hidden",true);},3000);};return;}else{if(ETparametersData!=null){var keys=Object.keys(ETparametersData);for(var elem=0;elem<keys.length;elem+=1){if(ETparametersData[keys[elem]].name=="SCHmodSett"){offVentSchedule=ETparametersData[keys[elem]].value;offVentScheduleName=ETparametersData[keys[elem]].name;offVentScheduleNum=keys[elem];break;}else if(ETparametersData[keys[elem]].name=="harmSett"){offVentSchedule=ETparametersData[keys[elem]].value;offVentScheduleName=ETparametersData[keys[elem]].name;offVentScheduleNum=keys[elem];break;};};if(offVentSchedule==1){$("#switchVentOnOffRadio").prop('checked',true);}else{$("#switchVentOnOffRadio").prop('checked',false);};};};var mode=$("#scheduleVENTMode").prop('selectedIndex');var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));$("#copySchedulesSelect").each(function(index,element){var option=$(element[dayNo]);option.prop('disabled',true);});$("#copySchedulesSelect").selectric("refresh");ventSchedulesData=params.values[0].slice();weeklyRanges=[[],[],[],[],[],[],[],[]];setVentSchedulesFlotDataDefault();prepareDailySeriesData();drawVentSchedule();};function drawVentSchedule(resizing){$('.ventModeSel').selectric({optionsItemBuilder:function(itemData){return itemData.value.length?'<span class="ico ico-'+itemData.value+'">'+translate(itemData.text)+'</span>'+'<div class="ico ico-'+itemData.value+'"></div>':itemData.text;},labelBuilder:function(currItem){return(currItem.value.length?'<span id="ventModeSelected">'+translate("mode")+': </span><span id="drawVentModeSelected'+currItem.value+'">'+translate(currItem.text)+'</span>'+'<div class="ico ico-'+currItem.value+'"></div>':'');}});$('.ventModeSel').selectric({disableOnMobile:false,nativeOnMobile:false});$('.ventModeSel').selectric('refresh');$('.hiddenOption').hide();resizeVentArea();plotSchedule();if(deleteMode==false){bindDrawPlotSelected();}else{bindDeletePlotClick();};};function bindDrawPlotSelected(){$('#scheduleVentPlaceholder').off('plotselected');$('#scheduleVentPlaceholder').off('plotclick');$('#scheduleVentPlaceholder').on('plotselected',function(event,ranges){var mode=$("#scheduleVENTMode").prop('selectedIndex');var from=Math.floor(ranges.xaxis.from*2)/2;var to=Math.floor(ranges.xaxis.to*2)/2;if(from<0){from=0;}
if(to>=24){to=23.5;}
var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));var freeRange=false;var rangesTmp=JSON.stringify(weeklyRanges[dayNo]);rangesTmp=JSON.parse(rangesTmp);var cutRanges=[];var clearRangesTMP=[0,0,0,0,0];var rangesNum=rangesTmp.length;for(var i=0;i<rangesNum;i++){range=rangesTmp[i];clearRangesTMP[range[2]]+=1;if(from<=range[0]&&to>=range[1]){cutRanges.push(i);clearRangesTMP[range[2]]-=2;}
else if(from>range[0]&&range[1]<=to&&from<=range[1]){rangesTmp[i][1]=from-0.5;}
else if(from<=range[0]&&to>=range[0]&&to<range[1]){rangesTmp[i][0]=to+0.5;}
else if(from>range[0]&&to<range[1]){rangesTmp.push([to+0.5,range[1],range[2]]);rangesTmp[i][1]=from-0.5;};};for(var i=(cutRanges.length-1);i>-1;i--){rangesTmp.splice(cutRanges[i],1);}
rangesTmp.push([from,to,mode])
rangesTmp=mergeRanges(from,to,mode,rangesTmp)
if(rangesTmp.length>5){plotSchedule();alert("No free range left");return;}else{weeklyRanges[dayNo]=rangesTmp;}
for(var i=0;i<ventSchedulesFlotData[dayNo].length;i++){ventSchedulesFlotData[dayNo][i]=[[0,0],[0.5,0],[1,0],[1.5,0],[2,0],[2.5,0],[3,0],[3.5,0],[4,0],[4.5,0],[5,0],[5.5,0],[6,0],[6.5,0],[7,0],[7.5,0],[8,0],[8.5,0],[9,0],[9.5,0],[10,0],[10.5,0],[11,0],[11.5,0],[12,0],[12.5,0],[13,0],[13.5,0],[14,0],[14.5,0],[15,0],[15.5,0],[16,0],[16.5,0],[17,0],[17.5,0],[18,0],[18.5,0],[19,0],[19.5,0],[20,0],[20.5,0],[21,0],[21.5,0],[22,0],[22.5,0],[23,0],[23.5,0]];}
for(var i=0;i<weeklyRanges[dayNo].length;i++){var series=ventSchedulesFlotData[dayNo].slice();ventSchedulesFlotData[dayNo][weeklyRanges[dayNo][i][2]]=setRange(weeklyRanges[dayNo][i],series[weeklyRanges[dayNo][i][2]]);}
plotSchedule();});};function bindDeletePlotClick(){$('#scheduleVentPlaceholder').off('plotselected');$('#scheduleVentPlaceholder').on('plotclick',function(event,pos,item){var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));var point=pos.x;var deleteIndexes=[];for(var i=0;i<weeklyRanges[dayNo].length;i++){if(point>=weeklyRanges[dayNo][i][0]&&point<=(weeklyRanges[dayNo][i][1]+0.5)){deleteIndexes.push(i);};};var deletelength=deleteIndexes.length;for(var i=deletelength-1;i>-1;i--){weeklyRanges[dayNo].splice(deleteIndexes[i],1);};for(var i=0;i<ventSchedulesFlotData[dayNo].length;i++){ventSchedulesFlotData[dayNo][i]=[[0,0],[0.5,0],[1,0],[1.5,0],[2,0],[2.5,0],[3,0],[3.5,0],[4,0],[4.5,0],[5,0],[5.5,0],[6,0],[6.5,0],[7,0],[7.5,0],[8,0],[8.5,0],[9,0],[9.5,0],[10,0],[10.5,0],[11,0],[11.5,0],[12,0],[12.5,0],[13,0],[13.5,0],[14,0],[14.5,0],[15,0],[15.5,0],[16,0],[16.5,0],[17,0],[17.5,0],[18,0],[18.5,0],[19,0],[19.5,0],[20,0],[20.5,0],[21,0],[21.5,0],[22,0],[22.5,0],[23,0],[23.5,0]];};for(var i=0;i<weeklyRanges[dayNo].length;i++){var series=ventSchedulesFlotData[dayNo].slice();ventSchedulesFlotData[dayNo][weeklyRanges[dayNo][i][2]]=setRange(weeklyRanges[dayNo][i],series[weeklyRanges[dayNo][i][2]]);};plotSchedule();});};function plotSchedule(){let safety=document.getElementById("scheduleVentPlaceholder");if((safety===null)||(safety.offsetWidth==0)||(safety.offsetHeight==0)){return;}
var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));var dataSet=[{data:seriesForHover,color:'white',bars:{show:true,barWidth:0.4},highlightColor:'RGB(213,214,216,0.4)'},{data:ventSchedulesFlotData[dayNo][0],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#03d4ee','#48759c']},highlightColor:'RGB(255,255,255,0.5)'},color:'#03d4ee'},{data:ventSchedulesFlotData[dayNo][1],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#d3f06c','#789616']},highlightColor:'RGB(255,255,255,0.5)'},color:'#d3f06c'},{data:ventSchedulesFlotData[dayNo][2],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#fad26f','#ed6819']},highlightColor:'RGB(255,255,255,0.5)'},color:'#fad26f'},{data:ventSchedulesFlotData[dayNo][3],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#f96f78','#bc1329']},highlightColor:'RGB(255,255,255,0.5)'},color:'#f96f78'},{data:ventSchedulesFlotData[dayNo][4],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#fa77c7','#962078']},highlightColor:'RGB(255,255,255,0.5)'},color:'#fa77c7'},];var dataSetOff=[{data:seriesForHover,color:'white',bars:{show:true,barWidth:0.4},highlightColor:'RGB(213,214,216,0.4)'},{data:ventSchedulesFlotData[dayNo][0],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#058a9a','#385a77']},highlightColor:'RGB(255,255,255,0.5)'},color:'#03d4ee'},{data:ventSchedulesFlotData[dayNo][1],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#8ca044','#52670f']},highlightColor:'RGB(255,255,255,0.5)'},color:'#d3f06c'},{data:ventSchedulesFlotData[dayNo][2],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#cead5d','#ad4e15']},highlightColor:'RGB(255,255,255,0.5)'},color:'#fad26f'},{data:ventSchedulesFlotData[dayNo][3],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#a74a50','#710d1a']},highlightColor:'RGB(255,255,255,0.5)'},color:'#f96f78'},{data:ventSchedulesFlotData[dayNo][4],bars:{show:true,barWidth:0.4,lineWidth:0,fillColor:{colors:['#b3558e','#6f1658']},highlightColor:'RGB(255,255,255,0.5)'},color:'#fa77c7'},];if($("#switchVentOnOffRadio").is(":checked")){plot=$.plot($("#scheduleVentPlaceholder"),dataSet,ScheduleChartVENTOptions);offVentSchedule=1;}else{plot=$.plot($("#scheduleVentPlaceholder"),dataSetOff,ScheduleChartVENTOptions);offVentSchedule=0;}
plot.clearSelection();plot.unhighlight();return;};function mergeRanges(from,to,mode,rng){var cutRanges=[];for(var i=0;i<(rng.length-1);i++){if(rng[i][2]==mode){if((rng[i][0]-0.5)==to){rng[rng.length-1][1]=rng[i][1];cutRanges.push(i)};if((rng[i][1]+0.5)==from){rng[rng.length-1][0]=rng[i][0];cutRanges.push(i);}};};for(var i=(cutRanges.length-1);i>-1;i--){rng.splice(cutRanges[i],1);}
return rng;};function prepareDailySeriesData(){for(var i=0;i<ventSchedulesData.length;i++){var ventRanges=ventSchedulesData[i].slice();for(var j=0;j<ventRanges.length;j++){var ventRng=ventRanges[j];var from=ventRng[0];var to=ventRng[1];var mode=ventRng[2];if(from[0]!=-1&&from[1]!=-1&&to[0]!=-1&&to[1]!=-1&&mode!=-1&&!(from[0]==to[0]&&from[1]==to[1])){var floatRange=prepareTimeRangesForChart(from,to);floatRange[0]=Math.round(floatRange[0]*2)/2;floatRange[1]=Math.round(floatRange[1]*2)/2-0.5;if(floatRange[1]<0){floatRange[1]=0;};floatRange.push(mode);weeklyRanges[i].push(floatRange);};};for(var k=0;k<weeklyRanges[i].length;k++){seriesTmp=ventSchedulesFlotData[i][weeklyRanges[i][k][2]].slice();ventSchedulesFlotData[i][weeklyRanges[i][k][2]]=setRange(weeklyRanges[i][k],seriesTmp);};};};function setRange(floatRange,seriesTmp){for(i=0;i<seriesTmp.length;i++){var item=seriesTmp[i];if(item[0]>=floatRange[0]&&item[0]<=floatRange[1]){seriesTmp[i][1]=1;};};return seriesTmp;};function prepareTimeRangesForChart(from,to){var fromHours=from[0];var fromMin=from[1];var toHours=to[0];var toMin=to[1];fromFloat=timeToFloat(fromHours,fromMin);toFloat=timeToFloat(toHours,toMin);var floatrange=[fromFloat,toFloat];return floatrange};function timeToFloat(hour,min){return floatTime=(hour*60+min)/60;};function drawModeSeries(series,from,to){var item;var checkIfClearOrDraw=0
for(var i=0;i<series.length;i++){item=series[i];if(item[0]>=from&&item[0]<to){if(checkIfClearOrDraw==0&&item[1]==0)
checkIfClearOrDraw=1;else if(checkIfClearOrDraw==0)
checkIfClearOrDraw=2;if(checkIfClearOrDraw==1){series[i][1]=1;}else if(checkIfClearOrDraw==2){series[i][1]=0;}}}
return series;};function resizeVentArea(){$("#scheduleVentPlaceholder").width($('#schedulesVentMain').width()/1.04);$("#scheduleVentPlaceholder").height($('#scheduleVentPlaceholder').width()/3);};function updateScheduleDayVent(dif){var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));var dayNoNew=(((dayNo+dif)%scheduleVentModes.length)+scheduleVentModes.length)%scheduleVentModes.length;$("#scheduleVentDayLabel").attr("value",dayNoNew);$("#scheduleVentDayLabel").text(translate(scheduleVentModes[dayNoNew]));$("#scheduleVentPlaceholder").off("plotselected");drawVentSchedule();};function deleteVentRanges(){if(deleteMode==false){deleteMode=true;drawVentSchedule();$("#deleteRangesVent").css('background-color','#06cce6');}else{deleteMode=false;drawVentSchedule();$("#deleteRangesVent").css('background-color','#2f323b');};};function saveSchedulesVent(){$("#saveSchedulesETBtn").attr("disabled",true);$("#saveSchedulesETBtn").removeClass("econetFormSaveSchedBtn");$("#saveSchedulesETBtn").addClass("econetFormSaveSchedBtnDisabled");$("#refreshScheduleVent").attr("disabled",true);$("#refreshScheduleVent").removeClass("deleteRangesVent");$("#refreshScheduleVent").addClass("refreshScheduleVentDisabled");$("#saveSchedulesVENTInfo").attr("hidden",false);saveSchedulesInterval=setInterval(function(){if(dots<3){$('#dots').append('.');dots++;}else{$('#dots').html('');dots=0;}},600);checkVentScheduleFlag=true;setTimeout(function(){checkVentScheduleFlag=false;unlockVentButtons();clearInterval(saveSchedulesInterval);},120000);ventSchedulesDatajson=schedulesToJson();var lastSchedule={value:ventSchedulesDatajson,timestamp:new Date().getTime()};localStorage.setItem("lastScheduleVent",JSON.stringify(lastSchedule));ETparametersData[parseInt(offVentScheduleNum)].value=offVentSchedule;controller.saveScheduleVent(ventSchedulesDatajson,offVentScheduleNum,offVentSchedule,saveSchedulesVentResponse);};function unlockVentButtons(){$("#saveSchedulesETBtn").attr("disabled",false);$("#saveSchedulesETBtn").removeClass("econetFormSaveSchedBtnDisabled");$("#saveSchedulesETBtn").addClass("econetFormSaveSchedBtn");$("#refreshScheduleVent").attr("disabled",false);$("#refreshScheduleVent").removeClass("refreshScheduleVentDisabled");$("#refreshScheduleVent").addClass("deleteRangesVent");$("#saveSchedulesVENTInfo").attr("hidden",true);}
function saveSchedulesVentResponse(response){};function refreshVentRanges(){weeklyRanges=[[],[],[],[],[],[],[],[]];setVentSchedulesFlotDataDefault();controller.getSchedules(getSchedulesResponse);};function schedulesToJson(){for(var i=0;i<ventSchedulesData.length;i++){for(var j=0;j<ventSchedulesData[i].length;j++){var rangeTmp=[];var fromTmp=[];var toTmp=[];if(typeof weeklyRanges[i][j]!=='undefined'){var from=weeklyRanges[i][j][0];var to=weeklyRanges[i][j][1]+0.5;var fromHours=Math.floor(from);var fromMin=from-fromHours;if(fromMin==0.5){fromMin=30;};fromTmp=[fromHours,fromMin];var toHours=Math.floor(to);var toMin=to-toHours;if(toMin==0.5){toMin=30;};if(toHours==24){toHours=23;toMin=59;};toTmp=[toHours,toMin];var mode=weeklyRanges[i][j][2];rangeTmp=[[fromHours,fromMin],[toHours,toMin],mode];}else{rangeTmp=[[-1,-1],[-1,-1],-1];};ventSchedulesData[i][j]=rangeTmp.slice();};};var ventSchedulesDatajson=JSON.stringify(ventSchedulesData)
return ventSchedulesDatajson;};function hideCopyForDays(){var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));$("#ventScheduleCopyForDaysContainer").attr("hidden",true);$("#day"+dayNo+"label").attr("hidden",false);$("#day"+dayNo+"selectSpan").attr("hidden",false);for(var i=0;i<=6;i++){if(document.getElementById('day'+i).checked){document.getElementById('day'+i).checked=false;};};};function copySelectedCopyForDays(){var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));for(var i=0;i<=6;i++){if(document.getElementById('day'+i).checked){weeklyRanges[i]=weeklyRanges[dayNo].slice();ventSchedulesFlotData[i]=ventSchedulesFlotData[dayNo].slice();document.getElementById('day'+i).checked=false;};};$("#ventScheduleCopyForDaysContainer").attr("hidden",true);};function copyVentRanges(){$("#ventScheduleCopyForDaysContainer").attr("hidden",false);var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));$("#day"+dayNo+"label").attr("hidden",true);$("#day"+dayNo+"selectSpan").attr("hidden",true);};function translateVentSchedules(){var dayNo=parseInt($("#scheduleVentDayLabel").attr("value"));$("#scheduleVentDayLabel").text(translate(scheduleVentModes[dayNo]));$("#saveSchedulesETBtn").text(translate("save"));$("#refreshScheduleVent").text(translate("submit_devfilter"));$("#copyScheduleVent").text(translate("copyForDay"));$("#deleteRangesVent").text(translate("deleteRanges"));$("#ventModeSelected").text(translate("mode"));$("#ventScheduleCopyForDaysHeader").text(translate("copyForDay")+":");$("#cancelCopyForDays").text(translate("cancel"));$("#saveCopyForDays").text(translate("copy"));$("#ventModeSelectedUser1").text(translate("User1"));$("#ventModeSelectedUser2").text(translate("User2"));$("#ventModeSelectedUser3").text(translate("User3"));$("#ventModeSelectedUser4").text(translate("User4"));$("#ventModeSelectedStop").text(translate("Stop"));$("#saveSchedulesVENTInfoLabel").text(translate("savingSchedule"));$("#saveSchedulesVENTInfSucces").text(translate("scheduleSaved"));for(var i=0;i<scheduleVentModes.length;i++){$("#day"+i.toString()+"label").text(translate(scheduleVentModes[i]));};};var updatesConfirmed={};var configSave=false;var configActSave=true;var configFabSave=true;var moduleToUpdate=null;var moduleWithConfigOpt=false;MODULES_NAMES={}
UPDATE_PROCESS_STATES=[]
UPDATE_NO_CONFIG_PROCESS_STATES=["soft_uploading","downloading_soft","checking_soft","conf_waiting","enter_bootloader","deleted_old_soft","flashing","verify_soft","finished","conf_upload_progress_cupl","end_upload_cupl"];UPDATE_WITH_CONFIG_PROCESS_STATES=["curr_config_copy","soft_uploading","downloading_soft","checking_soft","conf_waiting","enter_bootloader","deleted_old_soft","flashing","verify_soft","finished","auc_config_copy","config_prep_cupl","config_mod_upload_cupl","fabric_upload_cupl","current_upload_cupl","end_upload_cupl"];CONF_UPLOAD_PROCESS_STATES=["conf_uploading","downloading_soft","checking_soft","conf_upload_progress_cupl","end_upload_cupl"];CONFIG_SAVE_OPT_MODULES=["lbModuleAVerCurr"];CONFIG_LINKS={}
UPDATE_PROCESS_STATES_NOVISIBLE_KEYS=[]
function submitRegSoft(){clearConfUploadProgress();clearUpdateForDevice();var radiosavevalact=$("#softUpdateContent input[name='configsaverdact']:checked").val();var radiosavevalfab=$("#softUpdateContent input[name='configsaverdfab']:checked").val();if(updatesConfirmed[updater.currentDevice_]!=undefined){return;}
configSave=false;configActSave=true;configFabSave=true;moduleWithConfigOpt=false;CONFIG_LINKS={};moduleToUpdate=$("#moduleToUpdateSelect").val()
if(controller.protocol_type=="gm3_pomp"){configActSave=false;configFabSave=false;}
else{if(radiosavevalact.indexOf("yes")!=-1){configActSave=true;}else if(radiosavevalact.indexOf("no")!=-1){configActSave=false;}
if(radiosavevalfab.indexOf("yes")!=-1){configFabSave=true;}else if(radiosavevalfab.indexOf("no")!=-1){configFabSave=false;}}
if(configActSave||configFabSave){configSave=true;}else{configSave=false;}
reloadUpdateProgressList();if(CONFIG_SAVE_OPT_MODULES.indexOf(moduleToUpdate)!=-1&&controller.protocol_type!="gm3_pomp"){UPDATE_PROCESS_STATES=UPDATE_WITH_CONFIG_PROCESS_STATES;updateProcessInit("curr_config_copy");askForUpdateProgress();moduleWithConfigOpt=true;}else{moduleWithConfigOpt=false;UPDATE_PROCESS_STATES=UPDATE_NO_CONFIG_PROCESS_STATES;updateProcessInit("soft_uploading");}}
function reloadUpdateProgressList(){if(configSave){UPDATE_PROCESS_STATES_NOVISIBLE_KEYS=[]}else{UPDATE_PROCESS_STATES_NOVISIBLE_KEYS=['auc_config_copy']}
$("hr").remove();$("#updateProcessProgress").before("<hr>");$("#updateProcessProgress").after("<hr>");}
function updateProcessInit(startStatus){if(moduleToUpdate!=undefined&&moduleToUpdate!=null){var data=new FormData($("#regSoftForm")[0]);data.append("uid",updater.currentDevice_);data.append("module",moduleToUpdate);data.append("configActSave",configActSave);data.append("configFabSave",configFabSave);data.append("startStatus",startStatus);data.append("softFileName",$("#updateFileName").text())
if(startStatus!=null){writeUpdateResult(startStatus)}
updatesConfirmed[updater.currentDevice_]=false;disableUpdateInterface(true);controller.submitRegSoft(data);}}
function submitRegSoftResponse(result,textStatus,xmlhttprequest){if(result.result=='OK'){askForUpdateProgress();}else{setUpdateGlobalResultError(translate(result.error))}}
function submitRegConfig(){clearConfUploadProgress();clearUpdateForDevice();var data=new FormData($("#regConfigForm")[0]);data.append("uid",updater.currentDevice_);$("#configUploadProcessProgress").before("<hr>");$("#configUploadProcessProgress").after("<hr>");writeConfigUploadResult("conf_uploading","");controller.submitRegConfig(data);}
function submitRegConfigResponse(result,textStatus,xmlhttprequest){if(result.result=='OK'){$("#uploadProcessEndError").hide();$("#uploadProcessEndInfo").hide();askForConfigUploadProgress();}else if((result.error!=undefined)&&(result.error!=null)){setUploadGlobalResultError(result.error);}else{setUploadGlobalResultError('unknown_error');}}
function translateModulesList(){MODULES_NAMES={"lbModuleAVerCurr":translate("module")+" A","lbModuleBVerCurr":translate("module")+" B","lbModuleCVerCurr":translate("module")+" C","lbLambdaModuleVerCurr":translate("module")+" Lambda","lbEcoSTERModuleVerCurr":translate("module")+" ecoSTER","lbPanelModuleVerCurr":translate("module")+" Panel","lbPanel1ModuleVerCurr":translate("module")+" Panel 1","lbPanel2ModuleVerCurr":translate("module")+" Panel 2","lbPanel3ModuleVerCurr":translate("module")+" Panel 3","lbPanel4ModuleVerCurr":translate("module")+" Panel 4","lbPanel5ModuleVerCurr":translate("module")+" Panel 5","lbPanel6ModuleVerCurr":translate("module")+" Panel 6","lbPanel7ModuleVerCurr":translate("module")+" Panel 7","lbEcoSTERModuleVer1Curr":translate("module")+" ecoSTER 1","lbEcoSTERModuleVer2Curr":translate("module")+" ecoSTER 2","lbEcoSTERModuleVer3Curr":translate("module")+" ecoSTER 3","lbPanelVerCurr":translate("panel")}}
function createUploadFramesCode(descr){result_code=""
if(descr!=""){var descarr=descr.split(";")
for(var j=0;j<descarr.length;j++){var del=descarr[j]
var delarr=del.split(":");if(delarr.length==2){if(delarr[1]=="OK"){var div='<div style="padding: 3px;">'+translate(delarr[0])+'<span style="margin-left: 10px;">[<span style="color: #29db01">'+delarr[1]+'</span>]</span></div>';result_code+=div;}else if(delarr[1]=="FAIL"){var div='<div style="padding: 3px;">'+translate(delarr[0])+'<span style="margin-left: 10px;">[<span style="color: #FF0000">'+delarr[1]+'</span>]</span></div>';result_code+=div;}}else{var div='<div style="padding: 3px;">'+translate(delarr[0])+'</div>';result_code+=div;}}}
return result_code}
function writeConfigUploadResult(status,descrdata,prg_perc=null){var total_progres=""
if(CONF_UPLOAD_PROCESS_STATES.indexOf(status)!=-1){var stindex=CONF_UPLOAD_PROCESS_STATES.indexOf(status)
for(var i=0;i<CONF_UPLOAD_PROCESS_STATES.length;i++){var curr_el=CONF_UPLOAD_PROCESS_STATES[i]
if(i<=stindex){if(status.indexOf(curr_el)==-1){var div='<div style="padding: 3px;">'+translate(curr_el)+'<span style="margin-left: 10px;">[<span style="color: #29db01">OK</span>]</span></div>';total_progres+=div;}else{if(curr_el.indexOf("end_upload_cupl")!=-1&&curr_el.indexOf("download")==-1){var div=createUploadFramesCode(descrdata);div+='<div style="padding: 3px;">'+translate(curr_el)+'<span style="margin-left: 10px;">[<span style="color: #29db01">OK</span>]</span></div>';total_progres+=div;}else{if(prg_perc==null){var div='<div style="padding: 3px;">'+translate(curr_el)+'<img class="textPreloaders" src="/static/pict/loading.gif"></div>';total_progres+=div;}else{if(prg_perc>1.0){prg_perc=1.0;}
if(prg_perc<0.0){prg_perc=0.0;}
prg_perc=490.0*(1.0-prg_perc);var div='<div style="padding: 3px;">'+translate(curr_el)+'<svg class="textPreloaders" viewBox="0 0 200 200"><circle r="80" cx="100" cy="100" fill="transparent" stroke="#BBB" stroke-width="30"></circle><circle r="80" cx="100" cy="100" fill="transparent" stroke-dasharray="502.65" stroke-dashoffset="'+prg_perc+'" stroke="#111" stroke-width="30"></circle></svg></div>';total_progres+=div;}}}}}}
if(total_progres.length>0){$("#configUploadProcessProgress").html(total_progres)}}
function writeUpdateResult(result,descrdata=null,extrainfo=null,aupv=null,prg_perc=null){setUpdateGlobalResultInfo("");setUpdateGlobalResultError("");var fl_progress=null;var total_progres=""
if(result.indexOf("conf_upload_progress_cupl")!=-1){if(descrdata!=undefined){if(descrdata!=null){if(descrdata.length>0){if(descrdata.indexOf("0x96")!=-1){result='current_upload_cupl';}else{result='fabric_upload_cupl';}}else{result='fabric_upload_cupl';}}}}
if(UPDATE_PROCESS_STATES.indexOf(result)!=-1||result.indexOf("flashing")!=-1){for(var i=0;i<UPDATE_PROCESS_STATES.length;i++){var curr_el=UPDATE_PROCESS_STATES[i]
if(UPDATE_PROCESS_STATES_NOVISIBLE_KEYS.indexOf(curr_el)!=-1){continue;}
if(result.indexOf(curr_el)==-1||result.indexOf("finished")!=-1||result.indexOf("end_upload_cupl")!=-1){var status_info='<span style="color: #29db01">OK</span>';if(extrainfo!=undefined&&extrainfo!=null){if(typeof extrainfo=="string"){var extrainfo_obj=JSON.parse(extrainfo);if(extrainfo_obj[curr_el]!=undefined){var color='#29db01';if(extrainfo_obj[curr_el]=='FAIL'){color='#29db01';}
status_info='<span style="color: '+color+'">'+extrainfo_obj[curr_el]+'</span>'}}}
var div='';if(CONFIG_LINKS[curr_el]!=undefined&&CONFIG_LINKS[curr_el]!=null){var file_link='<a href="javascript:;" onclick="downloadConfigFileLink('+"'"+curr_el+"'"+');">Pobierz</a>'
div='<div style="padding: 3px;">'+translate(curr_el)+'<span style="margin-left: 10px;">['+status_info+']</span>'+file_link+'</div>'}else{div='<div style="padding: 3px;">'+translate(curr_el)+'<span style="margin-left: 10px;">['+status_info+']</span></div>'}
onclick="downloadDevConfigFile();"
total_progres+=div;}else{if(result.indexOf("flashing")!=-1){var div='<div style="padding: 3px;">'+translate(curr_el)+'</div><div id="progressbar_flashing"></div>'
var val_arr=result.split('_');if(val_arr.length>1){fl_progress=parseInt(val_arr[1])}
total_progres+=div;}else{if(prg_perc==null){var div='<div style="padding: 3px;">'+translate(curr_el)+'<img class="textPreloaders" src="/static/pict/loading.gif"></div>';total_progres+=div;}else{if(prg_perc>1.0){prg_perc=1.0;}
if(prg_perc<0.0){prg_perc=0.0;}
prg_perc=490.0*(1.0-prg_perc);var div='<div style="padding: 3px;">'+translate(curr_el)+'<svg class="textPreloaders" viewBox="0 0 200 200"><circle r="80" cx="100" cy="100" fill="transparent" stroke="#BBB" stroke-width="30"></circle><circle r="80" cx="100" cy="100" fill="transparent" stroke-dasharray="502.65" stroke-dashoffset="'+prg_perc+'" stroke="#111" stroke-width="30"></circle></svg></div>';total_progres+=div;}}
break;}}}
if(total_progres.length>0){$("#updateProcessProgress").html(total_progres)
if(fl_progress!=null){var bar1=$("#progressbar_flashing").progressbar();bar1.progress(fl_progress);}}
if(result=="finished"){if(!moduleWithConfigOpt){endUpdate();setUpdateGlobalResultInfo(translate("update_succesfully"));}}
if(result=="end_upload_cupl"){setUpdateGlobalResultInfo(translate("update_succesfully"));endUpdate();endConfigUpload();}}
function clearConfUploadProgress(){stopAskingForConfigUploadProgress();setUploadGlobalResultInfo("");setUploadGlobalResultError("");$("#configUploadProcessProgress").html("")
$("hr").remove();}
function clearUpdateForDevice(){setUpdateGlobalResultInfo("");setUpdateGlobalResultError("");stopAskingForProgress();updatesConfirmed[updater.currentDevice_]=undefined;$("#updateProcessProgress").html("")
$("hr").remove();}
function setUpdateGlobalResultInfo(resulttext){$("#updateProcessEndError").hide();$("#updateProcessEndInfo").hide();$("#updateProcessEndInfo").html(resulttext);if(resulttext.length>0){disableUpdateInterface(false);$("#updateProcessEndInfo").show();}}
function setUpdateGlobalResultError(resulttext){$("#updateProcessEndError").hide();$("#updateProcessEndInfo").hide();$("#updateProcessEndError").html(resulttext);if(resulttext.length>0){disableUpdateInterface(false);$(".updateProgressEl").replaceWith('<span style="margin-left: 10px;">[<span style="color: #FF0000">FAIL</span>]</span>');$("#updateProcessEndError").show();}}
function setUploadGlobalResultInfo(resulttext){$("#uploadProcessEndError").hide();$("#uploadProcessEndInfo").hide();$("#uploadProcessEndInfo").html(resulttext);if(resulttext.length>0){$("#uploadProcessEndInfo").show();}}
function setUploadGlobalResultError(resulttext){$("#uploadProcessEndError").hide();$("#uploadProcessEndInfo").hide();$("#uploadProcessEndError").html(resulttext);if(resulttext.length>0){$(".uploadProgressEl").replaceWith('<span style="margin-left: 10px;">[<span style="color: #FF0000">FAIL</span>]</span>');$("#uploadProcessEndError").show();}}
var updateProgress=undefined;var configUploadProgress=undefined;function askForUpdateProgress(){stopAskingForProgress();updateProgress=setInterval(function(){controller.getUpdateProgress(updater.currentDevice_,updateProgressResponse);},5000);}
function askForConfigUploadProgress(){disableUpdateInterface(true);stopAskingForConfigUploadProgress();configUploadProgress=setInterval(function(){controller.getUpdateConfigProgress(updater.currentDevice_,configUploadProgressResponse);},2500);}
function configUploadProgressResponse(result,textStatus,xmlhttprequest){var descr="";if(result==null){return;}
if(typeof result=="string"){result=JSON.parse(result);}
var prg=null;if(result.st_prg!=undefined){prg=result.st_prg;}
if(result.state=="canceled"){clearConfUploadProgress();return;}else if(result.error!=null){if(result.state!=undefined){writeConfigUploadResult(result.state,descr,prg);}
endConfigUpload();setUploadGlobalResultError(translate(result.error+"_cupl"));}else{if(result.state!=undefined&&result.state!=null){var descr="";if(result.upload_result!=undefined&&result.upload_result!=null)
descr=result.upload_result;writeConfigUploadResult(result.state,descr,prg);if(result.state=="end_upload_cupl"){endConfigUpload();}}}}
function configUploadStartProgressResponse(result,textStatus,xmlhttprequest){if(typeof result=="string"){result=JSON.parse(result);}
setUploadGlobalResultInfo("");setUploadGlobalResultError("");if(result==null||(result!=null&&result.state=="end_upload_cupl")){$("hr").remove();$("#configUploadProcessProgress").html("")}}
function updateProgressResponse(result,textStatus,xmlhttprequest){if(result==null){updatesConfirmed[updater.currentDevice_]=undefined;return;}
if(typeof result=="string"){result=JSON.parse(result);}
if(result.config_files_info!=undefined&&result.config_files_info!=null){CONFIG_LINKS={}
if(result.config_files_info.device_config!=undefined&&result.config_files_info.device_config){CONFIG_LINKS["curr_config_copy"]="device_config_";}
if(result.config_files_info.auc_device_config!=undefined&&result.config_files_info.auc_device_config){CONFIG_LINKS["auc_config_copy"]="auc_device_config_";}
if(result.config_files_info.cupl_device_config!=undefined&&result.config_files_info.cupl_device_config){CONFIG_LINKS["config_prep_cupl"]="cupl_device_config_";}}
if(result.state=="canceled"){clearUpdateForDevice();return;}
var prg=null;if(result.st_prg!=undefined){prg=result.st_prg;}
if((result.state=="version"||result.state=="conf_waiting")&&result.versions!=null&&!updatesConfirmed[updater.currentDevice_]==true){updatesConfirmed[updater.currentDevice_]=true;writeUpdateResult("conf_waiting");openConfirmPopup(result);}else if(result.error!=null){if(result.state!=undefined){writeUpdateResult(result.state,result.upload_result,result.extra_info,result.aupv,prg);}
setUpdateGlobalResultError(translate(result.error))}else{writeUpdateResult(result.state,result.upload_result,result.extra_info,result.aupv,prg);if((result.state=="finished"&&!moduleWithConfigOpt)||(result.state=="end_upload_cupl")){endUpdate();}else{console.log("NO UPDATE END")}}}
function endUpdate(){disableUpdateInterface(false);stopAskingForProgress();$("#preloaderUpdater").hide();updatesConfirmed[updater.currentDevice_]=undefined;}
function endConfigUpload(){disableUpdateInterface(false);stopAskingForConfigUploadProgress();}
function stopAskingForProgress(){if(updateProgress!=undefined){clearInterval(updateProgress);updateProgress=undefined;}}
function stopAskingForConfigUploadProgress(){if(configUploadProgress!=undefined){clearInterval(configUploadProgress);configUploadProgress=undefined;}}
function cancelUpdate(){controller.cancelUpdate(updater.currentDevice_);}
function cancelDevConfUpload(){controller.cancelDevConfUpload(updater.currentDevice_);}
function cancelUpdateResponse(result,textStatus,xmlhttprequest){disableUpdateInterface(false);}
function cancelDevConfUploadResponse(result,textStatus,xmlhttprequest){disableUpdateInterface(false);}
function confirmUpdateProcess(){closeUpdateConfTwoOptPopup();controller.confirmUpdate(updater.currentDevice_);}
function openUpdateWindow(){if(updatesConfirmed[updater.currentDevice_]==undefined){$('input:radio[name=configsaverdact][value=yes]').trigger("click");$('input:radio[name=configsaverdfab][value=yes]').trigger("click");}
translateModulesList();reloadSelectVersions();moduleSelChange();getUpdateStateElementDict();controller.isDevConfigFileExists(updater.currentDevice_,checkDeviceConfigResult,checkDeviceConfigError);}
function currUpdateProgressResponse(result,textStatus,xmlhttprequest){$("#updateProcessProgress").html("");if(typeof result=="string"){result=JSON.parse(result);}
var prg=null;setUpdateGlobalResultInfo("");setUpdateGlobalResultError("");$("hr").remove();let show_popup=false;if(result==null){updatesConfirmed[updater.currentDevice_]=undefined;disableUpdateInterface(false);}else{if(result.st_prg!=undefined){prg=result.st_prg;}
if(result.state.indexOf("finished")!=-1||result.state.indexOf("end_upload_cupl")!=-1){writeUpdateResult(result.state,result.upload_result,result.extra_info,result.aupv,prg);updatesConfirmed[updater.currentDevice_]=undefined;disableUpdateInterface(false);showTab('DevUpdate');if(result.state=="finished"){if(!moduleWithConfigOpt){endUpdate();return;}}
if(result.state=="end_upload_cupl"){endUpdate();endConfigUpload();return;}}
if(result.state!=undefined&&(UPDATE_PROCESS_STATES.indexOf(result.state)!=-1||result.state.indexOf("flashing")!=-1||result.state.indexOf("version")!=-1)){askForUpdateProgress();var currstate=result.state
if(currstate=="version")
currstate="conf_waiting"
writeUpdateResult(currstate,result.upload_result,result.extra_info,result.aupv,prg);}
$("#updateProcessProgress").before("<hr>");$("#updateProcessProgress").after("<hr>");if((result.state=="conf_waiting"||result.state=="version")&&result.versions!=null&&result.confirmed==undefined){updatesConfirmed[updater.currentDevice_]=false;show_popup=true;}else if(result.confirmed!=undefined&&result.confirmed){updatesConfirmed[updater.currentDevice_]=true;}else{updatesConfirmed[updater.currentDevice_]=false;}
disableUpdateInterface(true);}
showTab('DevUpdate');if(show_popup){openConfirmPopup(result);}}
function openConfirmPopup(result){openUpdateConfirmPopup(result.versions.oldVersionName.split(';').join('<br>'),result.versions.versionName.split(';').join('<br>'),MODULES_NAMES[moduleToUpdate]);}
function clearUpdatePanel(){$("#preloaderUpdater").hide();writeUpdateResult("");stopAskingForProgress();$("#regSoftFile").val(null);}
function checkUpdateResponse(result,textStatus,xmlhttprequest){if(result==""||result==null){return;}
$("#preloaderUpdater").show();updateProgressResponse(result,textStatus,xmlhttprequest);askForUpdateProgress();}
function getModuleActVer(key){for(var i in lastReadModulesVersions){var ver_desc=lastReadModulesVersions[i]
if(ver_desc!=null&&ver_desc.length>1){if(ver_desc[0].indexOf(key)!=-1){return' (ver. '+ver_desc[1]+')';}}}
return'';}
function translateUpdateSoftPanel(){translateModulesList();$("#sendRegSoftFile").val(translate("update"));$("#sendRegConfigFile").val(translate("upload"));$("#moduleToUpdateSelect option").each(function(){var rowtext=MODULES_NAMES[$(this).attr("value")]+getModuleActVer($(this).attr("value"))
$(this).text(rowtext);});$("#regSoftUpdateResult").text(translate($("#regSoftUpdateResult").attr("name")));$("#softUpdateModule").text(translate("soft_update_module"));}
(function($){$.fn.progressbar=function(options)
{var settings=$.extend({width:'50%',color:'#06cce6',padding:'3px',border:'1px solid #2f323b'},options);$(this).css({'width':settings.width,'border':settings.border,'overflow':'hidden','display':'inline-block','padding':settings.padding,'margin':'0px 10px 5px 5px'});var progressbar=$("<div></div>");progressbar.css({'height':settings.height,'text-align':'right','vertical-align':'middle','color':'#fff','width':'0px','background-color':settings.color});$(this).append(progressbar);this.progress=function(value)
{var width=$(this).width()*value/100;progressbar.width(width).html(value+"% ");}
return this;};}(jQuery));function changeSelFile(){$("#updateFileName").html($("#regSoftFile").val())}
function changeSelConfigFile(){$("#updateFileConfigName").html($("#regConfigFile").val())}
function selectRegSoft(){$("#regSoftFile").trigger("click");}
function selectConfigSoft(){$("#regConfigFile").trigger("click");}
function deviceConfigDownload(){controller.getDeviceConfig(updater.currentDevice_,getDeviceConfigResult,getDeviceConfigError,false);}
function getDeviceConfigResult(result,textStatus,xmlhttprequest){$("#deviceConfigDownloadLink").hide();if(result!=null){if(result.devconfig!=null){var data=result.devconfig;if(data=="inprogress"){setDeviceConfigState(true);}else if(data==true){setDeviceConfigState(false);}else if(data==false){setDeviceConfigState(false);}else{setDeviceConfigState(false);if(data=="downloaded"){controller.isDevConfigFileExists(updater.currentDevice_,checkDeviceConfigResult,checkDeviceConfigError);}}}else{setDeviceConfigState(false);}}else{setDeviceConfigState(false);}}
function setDeviceConfigState(devconfig){getEmDeviceConfig=devconfig;if(devconfig){$("#preloaderDeviceConfig").show();}else{$("#preloaderDeviceConfig").hide();}}
function getDeviceConfigError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);setDeviceConfigState(false);}
function downloadPrevUpdateFile(){let a=document.createElement("a");a.href=window.location.origin+"/aweb/f/legacy/oldconfig/"+updater.currentDevice_;document.body.appendChild(a);a.click();a.remove();}
function checkDeviceConfigResult(result,textStatus,xmlhttprequest){if(result!==null&&result!==undefined){if(result.devconfigexists==true){$("#deviceConfigDownloadLink").show();}else{$("#deviceConfigDownloadLink").hide();}
let dest=document.getElementById("deviceUpdateConfigDownloadLink");if(result.updateconfig!==null&&result.updateconfig!==undefined){let d=new Date(result.updateconfig);let dstr=d.getFullYear()+'-'+d.getMonth()+'-'+d.getDay()+' '+d.getHours()+':'+d.getMinutes();let dest_date=document.getElementById("deviceUpdateConfigDate");if(dest_date!==null&&dest_date!==undefined){dest_date.innerText=dstr;}
if(dest!==null&&dest!==undefined){dest.style.display=null;}}else{if(dest!==null&&dest!==undefined){dest.style.display="none";}}}}
function checkDeviceConfigError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);$("#deviceConfigDownloadLink").hide();}
function checkDeviceConfigDownloadResult(result,textStatus,xmlhttprequest){if(result!=null&&result.devconfigexists!=null){if(result.devconfigexists==true){window.location.href="/service/downloadDevConfigFile?uid="+updater.currentDevice_}else{$("#deviceConfigDownloadLink").hide();}}}
function getConfigFilesInfoDictResult(result,textStatus,xmlhttprequest){if(result!=null){if(result!=undefined&&result!=null){CONFIG_LINKS={}
if(result.device_config!=undefined&&result.device_config){CONFIG_LINKS["curr_config_copy"]="device_config_";}
if(result.auc_device_config!=undefined&&result.auc_device_config){CONFIG_LINKS["auc_config_copy"]="auc_device_config_";}
if(result.cupl_device_config!=undefined&&result.cupl_device_config){CONFIG_LINKS["config_prep_cupl"]="cupl_device_config_";}}}}
function getConfigFilesInfoDictError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);}
function getUpdateStateElementDictResult(result,textStatus,xmlhttprequest){if(result!=null){configActSave=result.actSave;configFabSave=result.fabSave;if(configActSave||configFabSave)
configSave=true;moduleToUpdate=result.module;$("#moduleToUpdateSelect").val(moduleToUpdate);$("#updateFileName").text(result.softFileName)
if(configActSave){$('input:radio[name=configsaverdact][value=yes]').trigger("click");}else{$('input:radio[name=configsaverdact][value=no]').trigger("click");}
if(configFabSave){$('input:radio[name=configsaverdfab][value=yes]').trigger("click");}else{$('input:radio[name=configsaverdfab][value=no]').trigger("click");}
if(CONFIG_SAVE_OPT_MODULES.indexOf(moduleToUpdate)!=-1&&controller.protocol_type!="gm3_pomp"){UPDATE_PROCESS_STATES=UPDATE_WITH_CONFIG_PROCESS_STATES;moduleWithConfigOpt=true;}else{moduleWithConfigOpt=false;UPDATE_PROCESS_STATES=UPDATE_NO_CONFIG_PROCESS_STATES;}
if(CONFIG_SAVE_OPT_MODULES.indexOf(moduleToUpdate)!=-1&&controller.protocol_type!="gm3_pomp"){$("#actRadioBtns").show();$("#fabRadioBtns").show();}else{$("#actRadioBtns").hide();$("#fabRadioBtns").hide();}}
controller.getUpdateProgress(updater.currentDevice_,currUpdateProgressResponse)}
function getUpdateStateElementDictError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);}
function downloadConfigFileLink(key){if(CONFIG_LINKS[key]!=undefined&&CONFIG_LINKS[key]!=null){var file_to_download=CONFIG_LINKS[key];window.location.href="/service/downloadDevConfigFile?uid="+updater.currentDevice_+"&key="+file_to_download;}}
function downloadDevConfigFile(){controller.isDevConfigFileExists(updater.currentDevice_,checkDeviceConfigDownloadResult,checkDeviceConfigError);}
function getDevConfigFilesInfoDict(){controller.getDevConfigFilesInfoDict(updater.currentDevice_,getConfigFilesInfoDictResult,getConfigFilesInfoDictError);}
function getUpdateStateElementDict(){controller.getUpdateStateElement(updater.currentDevice_,getUpdateStateElementDictResult,getUpdateStateElementDictError);}
function moduleSelChange(){if(CONFIG_SAVE_OPT_MODULES.indexOf($("#moduleToUpdateSelect").val())!=-1&&controller.protocol_type!="gm3_pomp"){$("#actRadioBtns").show();$("#fabRadioBtns").show();}else{$("#actRadioBtns").hide();$("#fabRadioBtns").hide();}}
function disableUpdateInterface(flag){$('#moduleToUpdateSelect').attr("disabled",flag);$('#configSelectButton').attr("disabled",flag);$('#softSelectBtn').attr("disabled",flag);$('#sendRegSoftFile').attr("disabled",flag);$('#sendRegConfigFile').attr("disabled",flag);$('#readConfButton').attr("disabled",flag);$('input:radio[name=configsaverdact]').attr("disabled",flag);$('input:radio[name=configsaverdfab]').attr("disabled",flag);}
var data_on_fuel_chart=[];var previousPoint=null;var diff=null;var org_diff=null;var fuelConsFromDateInput=null;var fuelConsToDateInput=null;var fuel_consum_grid_options={series:{bars:{show:true,barWidth:1000000,align:"center",fill:0.5,},color:'#00B4EE',},yaxis:{min:0,tickFormatter:fuel_consum_values_formatter},xaxis:{tickFormatter:fuel_consum_time_formatter,mode:"time",timezone:"browser",rotateTicks:90},grid:{color:"#363E45",backgroundColor:null,borderColor:"#363E45",hoverable:true,borderWidth:{top:0,left:2,bottom:2,right:0},labelMargin:20}};function resizeFuelConsumPlaceholder(){$("#placeholderFuelConsum").width($('#EmFuelConsumMain').width()/1.05);$("#placeholderFuelConsum").height($("#placeholderFuelConsum").width()/2.3);}
function initTabEmFuelConsum(){resizeFuelConsumPlaceholder();var pickerLang=(currLang=="cz")?"cs":currLang
if(fuelConsFromDateInput==null||(fuelConsFromDateInput!=null&&fuelConsFromDateInput.config.locale!=pickerLang)){fuelConsFromDateInput=flatpickr('#timePickerFromFuelConsum',{enableTime:true,time_24hr:true,locale:pickerLang,minuteIncrement:60})
if(fuelConsFromDateInput.minuteElement!=undefined){fuelConsFromDateInput.minuteElement.disabled=true}}
if(fuelConsToDateInput==null||(fuelConsToDateInput!=null&&fuelConsToDateInput.config.locale!=pickerLang)){fuelConsToDateInput=flatpickr('#timePickerToFuelConsum',{enableTime:true,time_24hr:true,locale:pickerLang,minuteIncrement:60})
if(fuelConsToDateInput.minuteElement!=undefined){fuelConsToDateInput.minuteElement.disabled=true}}
if(fuelConsFromDateInput.input.value.length==0||fuelConsFromDateInput.input.value.indexOf('NaN')!=-1||fuelConsToDateInput.input.value.length==0||fuelConsToDateInput.input.value.indexOf('NaN')!=-1){var fromDate;var toDate;fromDate=new Date($.now());fromDate.setHours(fromDate.getHours()-24);toDate=new Date($.now());fuelConsFromDateInput.setDate(zeroMinutes(fromDate));fuelConsToDateInput.setDate(zeroMinutes(toDate));}
if(data_on_fuel_chart.length==0){refreshFuelConsumValues();}else{drawEmFuelConsumChart([data_on_fuel_chart]);}}
function clearFuelConsumData(){data_on_fuel_chart=[];}
function drawEmFuelConsumChart(data){resizeFuelConsumPlaceholder();$("#placeholderFuelConsumDiv").show();$("#fuelConsumErr").hide();let safety=document.getElementById("placeholderFuelConsum");if((safety===null)||(safety.offsetWidth==0)||(safety.offsetHeight==0)){return;}
$.plot("#placeholderFuelConsum",data,fuel_consum_grid_options);$("#placeholderFuelConsum").on("plothover",function(event,pos,item){if(item){if(previousPoint!=item.dataIndex){previousPoint=item.dataIndex;$("#tooltip").remove();var date='';if(org_diff<24){date=js_yyyy_mm_dd(new Date(item.datapoint[0]))+" ("+dateXaxisFormater(new Date(item.datapoint[0]))+")";}else{date=js_yyyy_mm_dd(new Date(item.datapoint[0]));}
var value=item.datapoint[1].toFixed(2);showTooltipFC(item.pageX,item.pageY,'<span class="chartToolTipDate">'+date+'</span><span class="chartToolTipParamName"> '+value+" kg</span>");}}else{$("#tooltip").remove();previousPoint=null;}});}
function showTooltipFC(x,y,contents){$('<div id="tooltip">'+contents+'</div>').css({position:'absolute',display:'none',top:y+5,left:x+5,border:'1px solid #000000',padding:'4px','background-color':'#2f323b'}).appendTo("body").fadeIn(200);}
function fuel_consum_values_formatter(v,axis){return v.toFixed(2)+" kg";}
function fuel_consum_time_formatter(v,axis){var tickDate=new Date(v);if(tickDate<data_on_fuel_chart[0][0])
return"";if(org_diff<24){return dateXaxisFormater(new Date(v));}else{return js_yyyy_mm_dd(new Date(v));}}
function dateXaxisFormater(date){var startHour=date.getHours();var hdateTo=new Date(date.setHours(startHour+1));var endHour=hdateTo.getHours();return startHour+":00 - "+endHour+":00";}
function js_yyyy_mm_dd(date){year=""+date.getFullYear();month=""+(date.getMonth()+1);if(month.length==1){month="0"+month;}
day=""+date.getDate();if(day.length==1){day="0"+day;}
return year+"-"+month+"-"+day;}
function refreshFuelConsumValues(){showPreloader();var fdateZmin=zeroMinutes(getDateObjFromStr(fuelConsFromDateInput.input.value))
var tdateZmin=zeroMinutes(getDateObjFromStr(fuelConsToDateInput.input.value))
fuelConsFromDateInput.setDate(fdateZmin);fuelConsToDateInput.setDate(tdateZmin);var fromDate=toUTC(fdateZmin);var toDate=toUTC(tdateZmin);controller.getFuelConsumption(toISOString(fromDate),toISOString(toDate),getFuelConsumResponse,getFuelConsumError);}
function getFuelConsumResponse(result,textStatus,xmlhttprequest){clearFuelConsumData();drawChartFromFuelData(result.values,result.stvalues,result.fromDate,result.toDate);hidePreloader();}
function getFuelConsumError(jqXHR,textStatus,errorThrown){showErrorLabel(translate("data_download_failed"));}
function showErrorLabel(msg){hidePreloader();$("#placeholderFuelConsumDiv").hide();$("#fuelConsumErr").show();$("#fuelConsumErr").text(msg);}
function zeroMinutes(date){date.setMinutes(0);date.setSeconds(0);date.setMilliseconds(0);return date;}
function drawChartFromFuelData(values,stvalues,fromDate,toDate){if(values.length==0){showErrorLabel(translate("no_data_for_time_range"));return;}
values.sort(Comparator);let startDate=new Date(fromDate);let endDate=new Date(toDate)
endDate.setHours(endDate.getHours()-1);diff=org_diff=Math.ceil((endDate-startDate)/3600000);if(diff<24){data_on_fuel_chart=prepareValuesFromFuelConsum(values,startDate,endDate,'hour');fuel_consum_grid_options.series.bars.barWidth=3600000*(3/4);fuel_consum_grid_options.xaxis.minTickSize=[1,"hour"];}else{data_on_fuel_chart=prepareValuesFromFuelConsum(values,startDate,endDate,'day');fuel_consum_grid_options.series.bars.barWidth=3600000*24*(3/4);fuel_consum_grid_options.xaxis.minTickSize=[1,"day"];}
drawEmFuelConsumChart([data_on_fuel_chart]);}
function prepareValuesFromFuelConsum(values,startDate,endDate,period){if(period!='hour'&&period!='day'){period='day';}
zeroMinutes(startDate);zeroMinutes(endDate);if(period=='day'){startDate.setHours(0);endDate.setHours(0);}
let map={};let output=[];let currDate=new Date(startDate);let ii=0;while(currDate<=endDate){let key='';if(period=='day'){key=currDate.getFullYear()+'_'+currDate.getMonth()+'_'+currDate.getDate();}else{key=currDate.getFullYear()+'_'+currDate.getMonth()+'_'+currDate.getDate()+'_'+currDate.getHours();}
map[key]=ii;output.push([currDate.getTime(),0.0])
if(period=='day'){currDate.setTime(currDate.getTime()+25*3600000+5000);currDate.setHours(0);}else{currDate.setTime(currDate.getTime()+3600000+5000);}
zeroMinutes(currDate)
ii+=1;}
for(val of values){let key='';let currDate=new Date(val[0]);if(period=='day'){key=currDate.getFullYear()+'_'+currDate.getMonth()+'_'+currDate.getDate();}else{key=currDate.getFullYear()+'_'+currDate.getMonth()+'_'+currDate.getDate()+'_'+currDate.getHours();}
let pos=map[key];if(pos!==undefined){output[pos][1]+=val[1];}}
return output;}
function updateFuelCHartTranslation(){$('#refreshFuelConsum').text(translate("submit_devfilter"));$('#lbFromFuelConsum').text(translate('from'));$('#lbToFuelConsum').text(translate('to'));}