window.requestAnimFrame=(function(callback){return window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||function(callback){window.setTimeout(callback,1000/60);};})();var resizeEvt;window.addEventListener("resize",function(event){clearTimeout(resizeEvt);resizeEvt=setTimeout(function(){if(centerTiles()){tilesResChange=true;createTiles(tiles_tab);}
if(!$('#aMenu').is(':visible')){$('#deviceLeftPanelNavArea').show();}
if(window.innerWidth>1000){if(!$('#filtrOptions').is(':visible')){$('#filtrOptions').show();}}
$(".current").each(function(){if($(this).attr("id")=="tabHrChart"){initHeatChart();return;}
if($(this).attr("id")=="tabHrETChart"){resizeETPlot($(window).width(),$(window).height());return;}
if($(this).attr("id")=="tabHrSchedules"){drawSchedule();return;}
if($(this).attr("id")=="tabHrEmSchedules"){drawEmSchedule();return;}
if($(this).attr("id")=="tabHrETSchedules"){drawETSchedule(true);return;}
if($(this).attr("id")=="tabHrVentSchedules"){drawVentSchedule(true);return;}
if($(this).attr("id")=="tabHrEmFuelConsum"){drawEmFuelConsumChart([data_on_fuel_chart]);return;}});},250);});function showSettingsTab(){showTab('DevSettings');}
function showTab(tabName,tabHrName){if(tabHrName==undefined){tabHrName=tabName;}
$('#sec'+tabName).siblings('[id^="sec"]').hide();$('#sec'+tabName).show();$('#tabHr'+tabHrName).siblings().removeClass('current');$('#tabHr'+tabHrName).addClass('current');setWindowTitleFromNav();closeAllPopups();if(tabName!='Data'){$('#deviceBgElement').hide()
tilesStopAnimation();}else{$('#deviceBgElement').show()
centerTiles();tilesStartAnimation();}
if(tabName==='_ng_home'){$('#deviceBgElement').show()}
if(tabName==='DevSettings'&&remoteMenu){controller.getRemoteMenuExistingLangsList(langListResponse);}
if(tabName==='ServiceParams'){document.getElementById("serviceParamsMain").removeAttribute("data-user-authenticated");}else if(isDeviceGm3Conf()){lastETpasswordVal=null}
if(tabName=='Alarms'){updateAlarmsCall();}
if($('#aMenu').is(':visible')){$('#deviceLeftPanelNavArea').hide();}
if($('#deviceLeftPanelNavArea').css('display')=='none'){$('#alertBar').css('width','100%').css('float','right');}else{$('#alertBar').css('width','81%').css('float','right');}
$('#tooltip').hide();}
function openServiceParamsTab(){if(isDeviceGm3Conf()){if(lastETpasswordVal!=null){controller.getETPassword(checkLastETPasswordResponse);}else{showETPasswordPrompt();}}
else{showTab('ServiceParams','ServiceParams');}}
function showTabDevice(){$('#secData').siblings('[id^="sec"]').hide();$('#secData').show();$('#tabHrData').siblings().removeClass('current');$('#tabHrData').addClass('current');closeAllPopups();tilesStartAnimation();if($('#menuBtn').is(':visible'))
$('#mainMenu').hide();}
function showDevice(device){if(typeof thispage.reset_log=="function"){thispage.reset_log();}
if(isMemberOfGroup(GROUP_SERVICE)&&!isMemberOfGroup(GROUP_DEVICES)&&(device[1]==SERVICE_NOT_ALLOWED||updater.serviceAccess_==SERVICE_NOT_ALLOWED)){const modal=ngui.modal.make_abort("devices_modal");modal.text.style.display="flex";modal.text.style.gap="2em";const svg=ngui.svg.create_symbol("svg-symb-alarm","var(--color-cancel-bg-h)");svg.style.height="5em";modal.text.appendChild(svg);const text=document.createElement("div");ngt.prepare(text,"device_modal_access_not_allowed");modal.text.appendChild(text);ngui.modal.show("devices_modal");}else if(isMemberOfGroup(GROUP_SERVICE)&&!isMemberOfGroup(GROUP_PLUM)&&(device[1]==SERVICE_NOT_CLAIMED)){const modal=ngui.modal.make_abort("devices_modal");modal.text.style.display="flex";modal.text.style.gap="2em";const svg=ngui.svg.create_symbol("svg-symb-alarm","var(--color-cancel-bg-h)");svg.style.height="5em";modal.text.appendChild(svg);const text=document.createElement("div");ngt.prepare(text,"device_modal_access_not_owned");modal.text.appendChild(text);ngui.modal.show("devices_modal");}else{showMenu(null,'DevTabs',device[0],device[32],device[4],device[30]);let elem=document.getElementById("fix_ecosol_prodid");if(elem!==null){let softver=device[6].split('.').map(e=>Number(e));let correctsoft=(softver[0]==3)&&(softver[1]==4)&&(softver[2]>3827);if(correctsoft&&(device[4]=="gm3")){elem.style.display=null;}else{elem.style.display="none";}}
if(isMemberOfGroup(GROUP_SERVICE)){en300ng.check_updates(device[0]);let mx=document.getElementById("marketing_info");mx.children[1].children[5].children[0].href="/aweb/d/uid/v2/marketing_history?uid="+encodeURIComponent(device[0]);fetch("/aweb/d/uid/v2/marketing?uid="+encodeURIComponent(device[0]),{cache:"no-store"}).then(d=>{if(d.status!=200){return null;}return d.json();}).then(d=>{let mi=document.getElementById("marketing_info");if(d===null){mi.style.display="none";return;}
mi.style.display=null;let lst=mi.children[1];if(controller.only_device){if(d.valid_user){ngt.prepare(lst.children[1],"pg_marketing_status_verified");}else{ngt.prepare(lst.children[1],"pg_marketing_status_unverified");}
if(d.marketing){ngt.prepare(lst.children[3],"ui_lbl_allowed");}else{ngt.prepare(lst.children[3],"ui_lbl_not_allowed");}
if(d.contact_phone){lst.children[5].children[0].src="/static/pict/ui/market_phone_yes.svg";ngt.prepare(lst.children[5].children[1],"ui_lbl_allowed");}else{lst.children[5].children[0].src="/static/pict/ui/market_phone_no.svg";ngt.prepare(lst.children[5].children[1],"ui_lbl_not_allowed");}
if(d.contact_digital){lst.children[7].children[0].src="/static/pict/ui/market_digital_yes.svg";ngt.prepare(lst.children[7].children[1],"ui_lbl_allowed");}else{lst.children[7].children[0].src="/static/pict/ui/market_digital_no.svg";ngt.prepare(lst.children[7].children[1],"ui_lbl_not_allowed");}
let dt=new Date(d.changed_on*1000);lst.children[9].innerText=helpers.format_date(dt);}else{if(d.valid_user){ngt.prepare(lst.children[0].children[1],"pg_marketing_status_verified");}else{ngt.prepare(lst.children[0].children[1],"pg_marketing_status_unverified");}
if(d.marketing){ngt.prepare(lst.children[1].children[1],"ui_lbl_allowed");}else{ngt.prepare(lst.children[1].children[1],"ui_lbl_not_allowed");}
if(d.contact_phone){lst.children[2].children[1].children[0].src="/static/pict/ui/market_phone_yes.svg";ngt.prepare(lst.children[2].children[1].children[1],"ui_lbl_allowed");}else{lst.children[2].children[1].children[0].src="/static/pict/ui/market_phone_no.svg";ngt.prepare(lst.children[2].children[1].children[1],"ui_lbl_not_allowed");}
if(d.contact_digital){lst.children[3].children[1].children[0].src="/static/pict/ui/market_digital_yes.svg";ngt.prepare(lst.children[3].children[1].children[1],"ui_lbl_allowed");}else{lst.children[3].children[1].children[0].src="/static/pict/ui/market_digital_no.svg";ngt.prepare(lst.children[3].children[1].children[1],"ui_lbl_not_allowed");}
let dt=new Date(d.changed_on*1000);lst.children[4].children[1].innerText=helpers.format_date(dt);}}).catch(d=>{document.getElementById("marketing_info").style.display="none";console.log(d);});}}}
function showMenu(evt,name,dev_uid,prod_logo_id,protocol,ng_def=null){$("#tooltip").hide();if(evt){evt.stopPropagation();}
$('#s'+currentMenu).hide();$('#s'+name).show();$('#alertBar').css('width','100%');tilesStopAnimation();if(name=='Devices'){ngDevNfo.reset();const nghg=document.getElementById("ng_history_graph");const nght=document.getElementById("ng_history_timeline");ng_graph.core.clean(nghg.children[0],nght.children[0]);helpers.empty(nghg);const nghg_helper=document.createElement("span");ngt.prepare(nghg_helper,"pg_dev_hist_info");nghg.appendChild(nghg_helper);helpers.empty(nght);helpers.empty(document.getElementById("ng_history_selectors"));ngui.modal.hide("ng_history_modal");$('#topNavScrTitle').text("");$('#deviceLeftPanelMobileM').hide();if(remoteMenu){cleanRemoteMenuData();}
parameters_current=null;hideServicePanels();$("#cntrTime").hide();$('#activateTimer').hide();updateCurrentDevice();$("#topNavScrSubTitle").text("");$("#logoEconetPlum").show();$('#aDevices').hide()
controller.getDevices(createDevicesTable,devices_active,devices_notactive,devices_blocked,devices_deviceType,devices_uid,devices_prodId,devices_current_page,devices_softVer,$('#devfilter_ver_mod_a').val(),$('#devfilter_ver_panel').val());}
if(name=='DevTabs'){ngDevNfo.update(dev_uid,protocol);try{if(evt){ng_def=JSON.parse(evt.target.dataset.ng_def);}}catch{}
if(typeof ng_def!=='undefined'&&ng_def!==null){ngp_setup(ng_def,dev_uid);}
hideServicePanels();deviceClick(dev_uid,protocol,ng_def);$('#logoEconetPlum').hide();$("#ecoNetScrTitles").addClass('devSectionTitle');document.getElementById("logo").src='/static/pict/logos/logo_'+helpers.zerofill(prod_logo_id,3)+'-3x.jpg';}else{ngt.source_dynamic_clear();ngp_stop();$('#headerController').text('');$('#controllerLabel').hide();}
if(name=='Devices'){hideDeviceData();}
if(isMemberOfGroup(GROUP_DEVICES)){if(controller.protocol_type=="gm3_pomp"||controller.protocol_type=="gm3"){$("#showEconetRegDp").show();}else{$("#showEconetRegDp").hide();}}
currentMenu=name;}
function addTabToMenu(name){if($('#'+name).css('display')=='none'){$('#'+name).show();}}
function removeTabFromMenu(name){$('#'+name).hide();}
function showDataPreloader(){$('#preloaderdata').show();}
function hideDataPreloader(){$('#preloaderdata').hide();}
function showHistPreloader(value){$('#preloaderhist').show();}
function hideHistPreloader(){$('#preloaderhist').hide();}
var settings_ecosrv_soft_ver=null;var current_soft_ver='';var etNewConfTrans=false;var etConfVer=''
var regConfig=false;function updateEcosrvSoftVer(ecosrvSoftVer){settings_ecosrv_soft_ver=ecosrvSoftVer;if(current_soft_ver=='3.2.3810'){$('#newSoftUpdaterDl').show();$('#newSoftUpdater').hide();$('#newSoftVer').hide();}else if(current_soft_ver!='3.2.3810'&&current_soft_ver!=ecosrvSoftVer&&ecosrvSoftVer.length>0){$('#newSoftUpdaterDl').hide();$('#newSoftUpdater').hide();$('#newSoftVer').show();$('#lbNewSoftCounter').hide();$('#lbNewSoftVer').text(translate("new_soft_ver").replace('@newVer',settings_ecosrv_soft_ver));}else{$('#newSoftUpdaterDl').hide();$('#newSoftUpdater').hide();$('#newSoftVer').hide();}}
function checkSoftUpdateResponse(result,textStatus,xmlhttprequest){if(result.version!=null){updateEcosrvSoftVer(result.version);}}
function setDeviceNotWorkState(){$('#schemaInfo').hide();$('.mainTabView').hide();hidePreloader();}
function updateSysParamsCommon(result){if(result.regAllowed!=undefined&&!result.regAllowed){regAllowedAccess=result.regAllowed}
if(result.blocking!==undefined&&result.blocking){var $blockMessage=$("#devContent .lbDevBlocked");var $sections=$(".mainContentPanel section");$sections.each((index,element)=>{if(element.querySelector(".settingsMain")===null){var blockedMessage=element.querySelector(".lbDevBlocked");if(blockedMessage===null){var clonedElement=$blockMessage[0].cloneNode(true);$(clonedElement).show();element.appendChild(clonedElement);}else{$(blockedMessage).show();}}});$('.mainTabView').hide();$('.paramsMain').hide();$('.lbDevInactive').hide();$('.lbDevIncompatybile').hide();hidePreloader();}else
if(checkCurrentDevActive()){if(!regAllowedAccess){setDeviceNotWorkState();$('.lbDevInactive').hide();$('.lbDevIncompatybile').show();$('.lbDevBlocked').hide();$(".incompatybileView").hide();$("#tabHrSchedules").hide();$("#tabHrETSchedules").hide();$("#tabHrEmSchedules").hide();$("#tabHrVentSchedules").hide();$("#tabHrEmFuelConsum").hide();$("#tabHrServiceParams").hide();$("#tabHrUserParams").hide();}else{$('.lbDevInactive').hide();$('.lbDevIncompatybile').hide();$('.lbDevBlocked').hide();$('.mainTabView').show();$('.paramsMain').show();$('#schemaInfo').show();centerTiles();controller.setProtocolType(result.protocolType);controller.setType(result.regType);schema.controllerID=result.controllerID;schema.logoNum=result.prodLogo;if(result.modulesVers&&result.modulesVers.length>0){updateModulesVersionsFromArray(result.softVer,result.modulesVers,"devSettingsVersionsNrs");lastReadModulesVersions=result.modulesVers;}else{updateVersions(result.softVer,result.moduleASoftVer,result.moduleBSoftVer,result.moduleCSoftVer,result.moduleLambdaSoftVer,result.moduleEcoSTERSoftVer,result.modulePanelSoftVer);}
if(result.regAllowed==false){$('#deviceNotAllowedSecData').show();}else{$('#deviceNotAllowedSecData').hide();}
schemaUpdateView(result.schemaID,result.regType);if(result.tilesET!=undefined&&result.tilesET.length>0){tiles_tab=result.tilesET;createTilesET();tilesETFlag=true;}else{var tiles_names=createTiles(result.tiles);if(tiles_names!=null&&tiles_names.length>0){updater.currentTiles_=tiles_names;}
tilesETFlag=false;}
schemaUpdateValues();showHideMenuPos(result.softVer,result.fuelConsumptionCalc);}}else{setDeviceNotWorkState();$('.lbDevIncompatybile').hide();$('.lbDevBlocked').hide();$('.lbDevInactive').show();}}
function updateSysParamsCommonET(result){if(result.etNewConfTrans!=undefined){etNewConfTrans=result.etNewConfTrans;}
if(result.etConfVer!=undefined){etConfVer=result.etConfVer;$("#lbPanelDownlConfVerCurr").text(etConfVer);$("#trPanelDownlConfVer").show();}else{$("#lbPanelDownlConfVerCurr").text("");$("#trPanelDownlConfVer").hide();}
setPanelVer(result.panelVer,result.prodLogo,result.controllerID);updateSysParamsCommon(result);clearDict(SchemaParamsDict);SchemaParamsDict=result.schema;}
function clearDict(dict){for(var item in dict){delete dict[item];}}
function isDeviceGm3(){return updater!=undefined&&updater!=null&&(updater.controller_.protocol_type=="gm3"||updater.controller_.protocol_type=="gm3_pomp")}
function isDeviceGm3Conf(){return updater!=undefined&&updater!=null&&((updater.controller_.protocol_type=="gm3"&&regConfig)||updater.controller_.protocol_type=="gm3_pomp")}
SETTINGS_ECONET_UPDATE_SECONDS=240;function translateProfileForm(){$('#showEconetLogInp').val(translate("showEconetLog"));$('#deleteAlarmsButton').val(translate("delete_alarms"));$('#hideEconetLogInp').val(translate("hideEconetLog"));$('#showEconetLogFlInp').val(translate("showEconetLog")+"(flash)");$('#hideEconetLogFlInp').val(translate("hideEconetLog")+"(flash)");$('#showEconetBlWhListsInp').val(translate("show_access_lists"));$('#hideEconetBlWhListsInp').val(translate("hide_access_lists"));$('#showEconetRegDp').val(translate("show_regdp_lists"));$('#hideEconetRegDpInp').val(translate("hide_regdp_lists"));$('#saveBlWhListsInp').val(translate("save"));}
function translateSettings(){translateProfileForm();$('#service_params_access_label').text(translate("service_params_edit"));}
function startUpdateProcess(){controller.updateSoftware(updateSoftwareResponse,updateSoftwareError);}
function refreshUpdateCounter(uid,counter){if(counter>0){if(uid==updater.currentDevice_){$('#inpDownloadNewSoft').hide();var min=Math.floor(counter/60);var sec=counter%60;$('#lbNewSoftCounter').text(translate('econet_soft_updating')+(min>0?min+':':'')+(sec<10?'0'+sec:sec));$('#lbNewSoftCounter').show();}
--counter;setTimeout(function(){refreshUpdateCounter(uid,counter)},1000);}else{$('#lbNewSoftCounter').hide();}}
function updateSoftwareResponse(result,textStatus,xmlhttprequest){if(result=='OK'){refreshUpdateCounter(updater.currentDevice_,SETTINGS_ECONET_UPDATE_SECONDS);}else{console.log("updateSoftwareResponse(): Error! Result: "+result);var label=new ResultLabel($('#lbDevSettingsResult'));label.showError(translate('soft_update_failed'));}}
function updateSoftwareError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);var label=new ResultLabel($('#lbDevSettingsResult'));label.showError(translate('soft_update_failed'));}
function askEconetForLog(){controller.getEconetLog(updater.currentDevice_,showLog,getEconetLogError);}
function showLog(result,textStatus,xmlhttprequest){if(result!=null){if(result.log!=null){var data=result.log;if(data=="inprogress"){setEconetLogDownloadState(true);}else if(data==true){setEconetLogDownloadState(false);alert(translate("GettingLogTimeoutError"));}else if(data==false){setEconetLogDownloadState(false);alert(translate("GettingLogError"));}else{setEconetLogDownloadState(false);$("#econetGetEconetLogsControls").show();$("#econetLog").show();$("#hideEconetLogInp").show();$("#econetLog").text(result.log);}}else{setEconetLogDownloadState(false);}}else{setEconetLogDownloadState(false);}}
function hideEconetLog(){$("#econetLog").hide();$("#hideEconetLogInp").hide();$("#econetGetEconetLogsControls").hide();}
function setEconetLogDownloadState(state){getlogs=state;if(state){$("#preloaderLogs").show();}else{$("#preloaderLogs").hide();}}
function getEconetLogError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);setEconetLogDownloadState(false);}
function askEconetForRegDp(){controller.getEconetRegDp(updater.currentDevice_,showRegDp,getEconetRegDpError);}
function showRegDp(result,textStatus,xmlhttprequest){if(result!=null){if(result.dp!=null){var data=result.dp;if(data=="inprogress"){setEconetRegDpDownloadState(true);}else if(data==true){setEconetRegDpDownloadState(false);alert(translate("GettingLogTimeoutError"));}else if(data==false){setEconetRegDpDownloadState(false);alert(translate("GettingLogError"));}else{setEconetRegDpDownloadState(false);$("#econetGetEconetRegDpControls").show();$("#econetRegDp").show();$("#hideEconetRegDpInp").show();regDpData=JSON.parse(result.dp)
var dpArr=new Array()
for(var key in regDpData){var element_data=regDpData[key];if("minv"in element_data){var paramType=element_data.info&15;const paramArray=["??","i8","i16","i32","u8","u16","u32","f32","??","f64","bool","stringBCD","string","i64","u64","??"];var paramReadable=(element_data.info&16)>>>4;var paramWrittable=(element_data.info&32)>>>5;var additionalInfo=paramReadable?(paramWrittable?"MO":"O"):"-";dpArr.push([parseInt(key),"\t"+element_data.name,"\t"+"--","\t"+element_data.value,"\t"+"--","\t"+"","\t"+additionalInfo+" "+paramArray[paramType],"\t"+element_data.minv,"\t"+element_data.maxv,"\t"+element_data.minvDP,"\t"+element_data.maxvDP]);}else{dpArr.push([parseInt(key),element_data.name,element_data.value]);}}
dpArr.sort(function(a,b){return a[0]-b[0]});dpArr.unshift(["nr","\tnazwa","\tst","\twartosc","\tw","\tjedn.","\tinf.dod.","\tmin","\tmax","\tmin_DP","\tmax_DP"]);dpArr.forEach(element=>element.join(""))
$("#econetRegDp").text(dpArr.join("\n"));}}else{setEconetRegDpDownloadState(false);}}else{setEconetRegDpDownloadState(false);}}
function hideEconetRegDp(){$("#econetRegDp").hide();$("#hideEconetRegDpInp").hide();$("#econetGetEconetRegDpControls").hide();}
function setEconetRegDpDownloadState(state){getregdp=state;if(state){$("#preloaderRegDp").show();}else{$("#preloaderRegDp").hide();}}
function getEconetRegDpError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);setEconetRegDpDownloadState(false);}
function askEconetForBlWhLists(){controller.getBlWhLists(updater.currentDevice_,showBlWHLists,getBlWhListsError);$("#econetWhitelist").val("");$("#econetBlacklist").val("");}
function showBlWHLists(result,textStatus,xmlhttprequest){if(result!=null){if(result.lists!=null){var data=result.lists;if(data=="inprogress"){setBlWhDownloadState(true);}else if(data==true){setBlWhDownloadState(false);alert(translate("GettingLogTimeoutError"));}else if(data==false){setBlWhDownloadState(false);alert(translate("GettingLogError"));}else{setBlWhDownloadState(false);if(result.edit!=null){if(result.edit){$("#saveBlWhListsInp").show();}}
$("#econetAccessListsControls").show();$("#econetWhitelist").show();$("#econetBlacklist").show();$("#whiteListLabel").show();$("#blackListLabel").show();$("#hideEconetBlWhListsInp").show();$("#econetWhitelist").val((Object.keys(data).indexOf('whiteList')!=-1&&data.whiteList!=null)?data.whiteList:"");$("#econetBlacklist").val((Object.keys(data).indexOf('blackList')!=-1&&data.blackList!=null)?data.blackList:"");readErrors="";if('wherr'in data&&data.wherr!=null){readErrors+=data.wherr+"\n";}
if('blerr'in data&&data.blerr!=null){readErrors+=data.blerr+"\n";}
if(readErrors.length>0){alert(readErrors);}}}else{setBlWhDownloadState(false);}}else{setBlWhDownloadState(false);}}
function setBlWhDownloadState(state){getlists=state;if(state){$("#preloaderBlWhLists").show();}else{$("#preloaderBlWhLists").hide();}}
function getBlWhListsError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);var label=new ResultLabel($('#lbDevExtraSettingsResult'));label.showError(translate('GettingLogError'));setBlWhDownloadState(false);}
function hideEconetBlWhLists(){$("#econetWhitelist").text("");$("#econetBlacklist").text("");$("#econetWhitelist").hide();$("#econetBlacklist").hide();$("#whiteListLabel").hide();$("#blackListLabel").hide();$("#saveBlWhListsInp").hide();$("#hideEconetBlWhListsInp").hide();$("#econetAccessListsControls").hide();}
function hideServicePanels(){setEconetLogDownloadState(false);setBlWhDownloadState(false);hideEconetBlWhLists();hideEconetLog();clearUpdatePanel();setEconetLogFlDownloadState(false);$("#preloaderLogsStartFl").hide();$("#logFlInfo").hide();}
function saveEconetBlWhLists(){var whiteList=$("#econetWhitelist").val();var blackList=$("#econetBlacklist").val();controller.updateBlWhLists(whiteList,blackList,updater.currentDevice_,renewBlWhListsResponse,renewBlWhListsError);}
function renewBlWhListsResponse(result,textStatus,xmlhttprequest){var label=new ResultLabel($('#lbDevExtraSettingsResult'));if(result=='OK'){label.showInfo(translate('lists_renew_send'))}else{label.showError(translate('lists_renew_failed'));}}
function renewBlWhListsError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);var label=new ResultLabel($('#lbDevExtraSettingsResult'));label.showError(translate('lists_renew_failed'));}
function showHideDevAdminAreaButtons(){if(controller.protocol_type=="gm3_pomp"||controller.protocol_type=="gm3"){$("#showEconetRegDp").show();}else{$("#showEconetRegDp").hide();}}
function getAdvancedUserPassResponse(result,textStatus,xmlhttprequest){if(result.password!=''){$('#inpDevSettingsAdvancedUser').prop("checked",true);if(devices_dict[updater.currentDevice_]!=='undefined'){devices_dict[updater.currentDevice_].serviceParamsEdit=true;}}
else{$('#inpDevSettingsAdvancedUser').prop("checked",false);if(devices_dict[updater.currentDevice_]!=='undefined'){devices_dict[updater.currentDevice_].serviceParamsEdit=false;}}}
function validateAndSaveNewAdvancedPassword(){controller.changeAdvancedUserPass(updater.currentDevice_,$('#inpServicePasswd').val(),changeAdvancedUserPassResponse);}
function changeAdvancedUserPassResponse(result,textStatus,xmlhttprequest){if(result.hasOwnProperty("error")){showError('askPasswordWindowInfoArea',translate(result.error));}else{showEditParamConfirmLabelAndClose('#askPasswordWindowInfoArea','#secAskServicePassword');controller.getAdvancedUserPass(updater.currentDevice_,getAdvancedUserPassResponse);}}
function openDeleteAlarmsWarningPopup(){$('#twoOptPopupWindowTitle').text(translate('delete_alarms'));$('#twoOptPopupContentArea').text(translate('delete_alarms_warning'));$("#twoOptPopupOK").text(translate('yes'));$("#twoOptPopupCancel").text(translate('no'));prepareTwoOptPopup("deleteAlarmsConf();","closeTwoOptPopup(); return false;",{"name":"delete_alarms"})
openTwoOptPop();}
function deleteAlarmsConf(){deleteAlarms();closeTwoOptPopup();}
function deleteAlarms(){if(updater.currentDevice_!=undefined){controller.deleteDevAlarms(updater.currentDevice_,deleteAlarmsResponse);}}
function deleteAlarmsResponse(result,textStatus,xmlhttprequest){var label=new ResultLabel($('#deleteAlarmsInfo'));if(result==true){label.showInfo(translate("alarms_deleted_success"));}
else{label.showError(translate("alarms_deleted_error"));}}
function langListResponse(result,textStatus,xmlhttprequest){if(result!=null){if(result.error==null){$('#trLangSelection').show()
$('#selLangs option').each(function(i){if($(this).val()!="default"&&$(this).val()!="nosel")
$(this).remove();});var firstValue="default";if(result.length>0){langs_list=result;for(n in langs_list){var newOption=$('<option value="'+langs_list[n].code+'">'+langs_list[n].name+'</option>');$('#selLangs').append(newOption)}
$('#selLangs').val(remoteManuLang)
$('#selLangs').selectric('refresh');}}}}
function saveSelectedRemoteMenuLang(){Cookies.set(updater.currentDevice_+"_language",$('#selLangs').val(),{expires:new Date(9999,12,31,23,59,59)});}
function rmLangChanged(){remoteManuLang=$('#selLangs').val();setRemoteMenuCurrentLanguage();reloadRemoteMenuData();}
function loadRmLangFromCookie(){if(Cookies.get(updater.currentDevice_+"_language")!=undefined){remoteManuLang=Cookies.get(updater.currentDevice_+"_language");setRemoteMenuCurrentLanguage();}}
function getRmLang(){if(remoteManuLang!="nosel"){if(remoteManuLang=="default"){return remoteMenuDefaultLang;}else{return remoteManuLang;}}else{if(currLang in langs_code_trans){if(currLangcodeInLangList()){return langs_code_trans[currLang]}else{return remoteMenuDefaultLang;}}else{if(remote_menu_current_language_version!=""){if(currLangcodeInLangList()){return currLang}else{return remoteMenuDefaultLang;}}else{return remoteMenuDefaultLang;}}}}
function restartDevice(){controller.restartDevice(restartDeviceResult,restartDeviceError);}
function restartDeviceResult(result,textStatus,xmlhttprequest){if(result.result=='OK'){refreshRestartCounter(updater.currentDevice_,SETTINGS_ECONET_UPDATE_SECONDS,'restartDeviceInfo','restartDeviceButton');}else{console.log("updateSoftwareResponse(): Error! Result: "+result.error);var label=new ResultLabel($('#restartDeviceInfo'));label.showError(result.error);}
closeTwoOptPopup();}
function restartDeviceError(jqXHR,textStatus,errorThrown){logError(jqXHR,textStatus,errorThrown);var label=new ResultLabel($('#restartDeviceInfo'));label.showError(translate('device_restart_failed'));}
function refreshRestartCounter(uid,counter,label,button){if(counter>0){if(uid==updater.currentDevice_){$('#'+button).hide();var min=Math.floor(counter/60);var sec=counter%60;$('#'+label).text(translate('econet_restart')+': '+(min>0?min+':':'')+(sec<10?'0'+sec:sec));$('#'+label).show();}
--counter;setTimeout(function(){refreshRestartCounter(uid,counter,label,button)},1000);}else{$('#'+label).hide();$('#'+button).show();}}
var logFlState=false;function startEconetLogFl(){if(!logFlState){controller.startEconetLogFl(startEconetLogFlResponse,startEconetLogFlError);}
else{controller.stopEconetLogFl(startEconetLogFlResponse,startEconetLogFlError);}}
function startEconetLogFlResponse(result,textStatus,xmlhttprequest){$("#preloaderLogsStartFl").show();}
function startEconetLogFlError(jqXHR,textStatus,errorThrown){$("#preloaderLogsStartFl").hide();logError(jqXHR,textStatus,errorThrown);$("#logFlInfo").text(translate("failed_log_fl"));$("#logFlInfo").show();}
function updateLogFlState(value){if(logFlState!=value){$("#preloaderLogsStartFl").hide();logFlState=value;if(value==1){$("#logFlInfo").text(translate("save_log_fl"));$("#logFlInfo").show();$("#startEconetLogFlInp").val(translate("stop_log_fl"));}
else{$("#logFlInfo").hide();$("#startEconetLogFlInp").val(translate("start_log_fl"));}}}
function askEconetForLogFl(){controller.getEconetLogFl(askEconetForLogFlResponse,askEconetForLogFlError)}
function askEconetForLogFlError(jqXHR,textStatus,errorThrown){$("#preloaderLogsFl").hide();logError(jqXHR,textStatus,errorThrown);}
function askEconetForLogFlResponse(result,textStatus,xmlhttprequest){if(result!=null){if(result.log!=null){var data=result.log;if(data=="inprogress"){setEconetLogFlDownloadState(true);}else if(data==true){setEconetLogFlDownloadState(false);alert(translate("GettingLogTimeoutError"));}else if(data==false||data=="no_log"){setEconetLogFlDownloadState(false);alert(translate("GettingLogError"));}else{setEconetLogFlDownloadState(false);$("#econetGetEconetLogsFlControls").show();$("#econetLogFl").show();$("#hideEconetLogFlInp").show();$("#econetLogFl").text(result.log);}}else{setEconetLogFlDownloadState(false);}}else{setEconetLogFlDownloadState(false);}}
function hideEconetLogFl(){$("#econetLogFl").hide();$("#hideEconetLogFlInp").hide();$("#econetGetEconetLogsFlControls").hide();}
function setEconetLogFlDownloadState(state){getlogsfl=state;if(state){$("#preloaderLogsFl").show();}else{$("#preloaderLogsFl").hide();}}
var GROUP_ROOT='root';var GROUP_SERVICE='service';var GROUP_DEVICES='devices';var GROUP_MANAGEMENT='management';var GROUP_PRODUCER='producer';var GROUP_DEMO='demo';var updater=null;var controller=new Controller(window.location.protocol+"//"+window.location.host+"/service/",window.location.host);function isNotAnonymous(){var _tmp=$('#hfGroups').val();if((_tmp===undefined)||(_tmp===null)){return false;}
return true;}
function isMemberOfGroup(group){var _tmp=$('#hfGroups').val();if((_tmp===undefined)||(_tmp===null)){return false;}
try{_tmp=JSON.parse(_tmp);}catch{return false;}
return _tmp.includes(group)}
function isNormalUser(){var _tmp=$('#hfGroups').val();if((_tmp===undefined)||(_tmp===null)){return false;}
try{_tmp=JSON.parse(_tmp);}catch{return false;}
return _tmp.length==0;}
function isDemoUser(){var _tmp=$('#hfGroups').val();if((_tmp===undefined)||(_tmp===null)){return false;}
try{_tmp=JSON.parse(_tmp);}catch{return false;}
return _tmp.includes(GROUP_DEMO)&&!_tmp.includes(GROUP_ROOT);}
function isServiceUser(){var _tmp=$('#hfGroups').val();if((_tmp===undefined)||(_tmp===null)){return false;}
try{_tmp=JSON.parse(_tmp);}catch{return false;}
return _tmp.includes(GROUP_SERVICE)&&!_tmp.includes(GROUP_ROOT);}
function isNotNormalUserNorAdmin(){var _tmp=$('#hfGroups').val();if((_tmp===undefined)||(_tmp===null)){return false;}
try{_tmp=JSON.parse(_tmp);}catch{return false;}
return(_tmp.length!=0)&&!_tmp.includes(GROUP_ROOT);}
var ECOSRV_REFRESH_PERIOD=10000;var GROUP_ROOT='root';var GROUP_SERVICE='service';var GROUP_DEVICES='devices';var GROUP_MANAGEMENT='management';var GROUP_PRODUCER='producer';var GROUP_DEMO='demo';var GROUP_PLUM='plum';var STATE_NOT_ACTIVE='not_active';var STATE_BLOCKED='blocked';var updater=new CurrentViewUpdater(controller,ECOSRV_REFRESH_PERIOD);var schema=new Schema(window.location.protocol+'//'+window.location.host+'/static/pict/schema/');var currentMenu='Devices';var wavePict=window.location.protocol+'//'+window.location.host+'/static/pict/waves.svg';var getlists=false;var getlogs=false;var getlogsfl=false;var getregdp=false;var getEmDeviceConfig=false;var schemaVentFlag=false;var checkVentScheduleFlag=false;var disabledList={};remoteMenu=false;regAllowedAccess=true;var remote_menu_languages=null;var remote_menu_default_language_version='';var remote_menu_current_language_version='';window.onerror=function myErrorHandler(errorMsg,url,lineNumber){console.log("ERROR: "+errorMsg+" "+url+" line: "+lineNumber);return false;}
var REMOTE_MENU_PARAMS_LANGS_="1";var REMOTE_MENU_PARAMS_NAMES_="2";var REMOTE_MENU_PARAMS_VALUES_="3/4";var REMOTE_MENU_PARAMS_UNITS_NAMES_="6";var REMOTE_MENU_ENUMS_NAMES_="7";var REMOTE_MENU_CATS_NAMES_="8";var REMOTE_MENU_STRUCTURE_="9";var REMOTE_MENU_CURRDATA_DISP_="11";var REMOTE_MENU_ALARMS_NAMES_="12";var REMOTE_MENU_PARAMS_DESCS_="13";var REMOTE_MENU_CATS_DESCS_="14";var REMOTE_MENU_LOCKS_NAMES_="15";function CurrentViewUpdater(controller,period){this.controller_=controller;this.repeatPeriod_=period;this.currentDevice_=undefined;this.settingsParamsVer_=-1;this.editableParamsVer_=-1;this.currentParamsVer_=-1;this.schedulesVer_=-1;this.remoteMenuVer_={}
this.currParamsEditsVer_=-1;this.currentTiles_=[];this.setDeviceId=function(uid){this.currentDevice_=uid;loadRmLangFromCookie();this.refreshDeviceVersions();};this.refreshDeviceVersions=function(){this.settingsParamsVer_=-1;this.editableParamsVer_=-1;this.currentParamsVer_=-1;this.schedulesVer_=-1;this.remoteMenuVer_={}
this.currParamsEditsVer_=-1;this.blocking_=false;}
this.updateDev=function(){this.controller_.getDeviceParams(this.currentDevice_,this.refreshDeviceParams.bind(this));};this.doUpdate=function(){var self=this;setTimeout(function(){self.doUpdate();},this.repeatPeriod_);this.controller_.getCurrentState(this.refreshCurrentState.bind(this));if(this.currentDevice_){this.updateDev();}};this.refreshCurrentState=function(result,textStatus,xmlhttprequest){if(result.logged_in){}else{window.location=window.location.protocol+'//'+window.location.host+'/login';}};this.reloadRemoteMenuTexts=function(){if(!(REMOTE_MENU_PARAMS_NAMES_ in this.remoteMenuVer_)||(REMOTE_MENU_PARAMS_NAMES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_PARAMS_NAMES_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuParamsNames(getRemoteMenuParamsNamesResponse);}
if(!(REMOTE_MENU_CATS_NAMES_ in this.remoteMenuVer_)||(REMOTE_MENU_CATS_NAMES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_CATS_NAMES_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuCatsNames(getRemoteMenuCatsNamesResponse);}
if(!(REMOTE_MENU_PARAMS_UNITS_NAMES_ in this.remoteMenuVer_)||(REMOTE_MENU_PARAMS_UNITS_NAMES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_PARAMS_UNITS_NAMES_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuParamsUnitsNames(getRemoteMenuParamsUnitsNamesResponse);}
if(!(REMOTE_MENU_ENUMS_NAMES_ in this.remoteMenuVer_)||(REMOTE_MENU_ENUMS_NAMES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_ENUMS_NAMES_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuParamsEnums(getRemoteMenuParamsEnumsResponse);}
if(!(REMOTE_MENU_LOCKS_NAMES_ in this.remoteMenuVer_)||(REMOTE_MENU_LOCKS_NAMES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_LOCKS_NAMES_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuLocksNames(getRemoteMenuLocksNamesResponse);}
if(!(REMOTE_MENU_CURRDATA_DISP_ in this.remoteMenuVer_)||(REMOTE_MENU_CURRDATA_DISP_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_CURRDATA_DISP_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuCurrDataDisp(getRemoteMenuCurrDataDispResponse);}
if(!(REMOTE_MENU_PARAMS_DESCS_ in this.remoteMenuVer_)||(REMOTE_MENU_PARAMS_DESCS_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_PARAMS_DESCS_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuParamsDescs(getRemoteMenuParamsDescsResponse);}
if(!(REMOTE_MENU_CATS_DESCS_ in this.remoteMenuVer_)||(REMOTE_MENU_CATS_DESCS_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_CATS_DESCS_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuCatsDescs(getRemoteMenuCatsDescsResponse);}
if(!(REMOTE_MENU_ALARMS_NAMES_ in this.remoteMenuVer_)||(REMOTE_MENU_ALARMS_NAMES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_ALARMS_NAMES_]!=remote_menu_current_language_version)){this.controller_.getRemoteMenuAlarmsNames(getRemoteMenuAlarmsNamesResponse);}
updateRemoteMenuView()}
this.refreshDeviceParams=function(resp,textStatus,xmlhttprequest){if(resp.remoteMenu!=undefined){remoteMenu=resp.remoteMenu;}
reloadParamsEnableState(resp.changedParams)
if(this.currentParamsVer_!=resp.currentParamsVer){setParamAndUpdate(resp.curr,resp.currUnits,resp.currNumbers,resp.schemaParams,resp.tilesParams);if((this.settingsParamsVer_==resp.settingsParamsVer)&&(this.editableParamsVer_==resp.editableParamsVer)){this.currentParamsVer_=resp.currentParamsVer;}}
if(!controller.only_device){wifiInfoRefresh(resp.wifiQuality,resp.wifiStrength)}
if(this.settingsParamsVer_!=resp.settingsParamsVer){this.controller_.getDeviceSysParams(this.currentDevice_,updateDeviceSysParams);}
if((this.editableParamsVer_!=resp.editableParamsVer)){this.controller_.getDeviceEditableParams(this.currentDevice_,getEditParamsResponse);}
if(getlists){this.controller_.getBlWhLists(this.currentDevice_,showBlWHLists,getBlWhListsError);}
if(getlogs){this.controller_.getEconetLog(this.currentDevice_,showLog,getEconetLogError);}
if(getlogsfl){this.controller_.getEconetLogFl(askEconetForLogFlResponse,askEconetForLogFlError);}
if(getregdp){this.controller_.getEconetRegDp(this.currentDevice_,showRegDp,getEconetRegDpError);}
if(getEmDeviceConfig){deviceConfigDownload();}
if(remoteMenu&&resp.remoteMenuVer!=undefined&&resp.remoteMenuVer!={}){this.controller_.getDeviceRegParams(this.currentDevice_,getRegParamsDataResponse);if(REMOTE_MENU_PARAMS_LANGS_ in resp.remoteMenuVer){if(!(REMOTE_MENU_PARAMS_LANGS_ in this.remoteMenuVer_)||(REMOTE_MENU_PARAMS_LANGS_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_PARAMS_LANGS_]!=resp.remoteMenuVer[REMOTE_MENU_PARAMS_LANGS_])){this.controller_.getRemoteMenuLangs(getRemoteMenuLangListResponse);}}
if(REMOTE_MENU_STRUCTURE_ in resp.remoteMenuVer){if(!(REMOTE_MENU_STRUCTURE_ in this.remoteMenuVer_)||(REMOTE_MENU_STRUCTURE_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_STRUCTURE_]!=resp.remoteMenuVer[REMOTE_MENU_STRUCTURE_])){this.controller_.getRemoteMenuStructure(getRemoteMenuStructureResponse);}}
if(REMOTE_MENU_PARAMS_VALUES_ in resp.remoteMenuVer){if(!(REMOTE_MENU_PARAMS_VALUES_ in this.remoteMenuVer_)||(REMOTE_MENU_PARAMS_VALUES_ in this.remoteMenuVer_&&this.remoteMenuVer_[REMOTE_MENU_PARAMS_VALUES_]!=resp.remoteMenuVer[REMOTE_MENU_PARAMS_VALUES_])){this.controller_.getRemoteMenuParamsData(getRemoteMenuParamsDataResponse);}}
if(remote_menu_languages!=null){this.reloadRemoteMenuTexts()}}
if(resp.currentDataParamsEditsVer!=undefined){if(this.currParamsEditsVer_!=resp.currentDataParamsEditsVer){this.controller_.getCurrentParamsEdits(getCurrentParamsEditsResponse);}}
if(checkCurrentDevActive()&&regAllowedAccess&&(controller.protocol_type=="gm3"||controller.protocol_type=='em')&&this.schedulesVer_!=resp.schedulesParamsVer){updateSchedulesCall();}else if(checkVentScheduleFlag==true&&checkCurrentDevActive()&&regAllowedAccess&&controller.protocol_type=="gm3_pomp"){controller.getSchedules(getSchedulesResponse);};tiles_currentDataUpdate+=1;};}
function watchChangedParamsValues(){if(!$.isEmptyObject(changedParams)){var keys=Object.keys(changedParams);for(key in keys){if(keys[key]in changedParamsCounters){changedParamsCounters[keys[key]]++;}else{changedParamsCounters[keys[key]]=1;}}
var ckeys=Object.keys(changedParamsCounters);var reloadUI=false;for(ckey in ckeys){if(changedParamsCounters[ckeys[ckey]]>30){delete changedParams[ckeys[ckey]]
delete changedParamsCounters[ckeys[ckey]]
reloadUI=true;}}
if(reloadUI){updater.refreshDeviceVersions();}}else{changedParamsCounters={}}}
function reloadParamsEnableState(srvChangedParams){if(!$.isEmptyObject(changedParams)){if(isDeviceGm3Conf()){if(srvChangedParams!=undefined&&!$.isEmptyObject(srvChangedParams)){for(param in changedParams){var paramobj=changedParams[param]
if(paramobj.index!=undefined){var keystr=paramobj.index.toString()
if(!findChangedParamInSrvData(srvChangedParams,keystr)){tilesReload=enableParamControls(param);}}}}else{var keys=Object.keys(changedParams);for(var key in keys){var keystr=keys[key];tilesReload=enableParamControls(keystr);}}}else{var keys=Object.keys(changedParams);var tilesReload=false;if(srvChangedParams!=undefined&&!$.isEmptyObject(srvChangedParams)){for(var key in keys){var keystr=keys[key]
if(!findChangedParamInSrvData(srvChangedParams,keystr)){if(changedParams[keystr].type==STANDARD_PARAM_NAME_TYPE){tilesReload=enableParamControls(keystr);}}}}else{for(var key in keys){var keystr=keys[key];if(changedParams[keystr].type==STANDARD_PARAM_NAME_TYPE){tilesReload=enableParamControls(keystr);}}}}
if(tilesReload){updateStatic();}}}
function showHideMenuPos(econetVer,fuelCalculate){if(fuelCalculate!=undefined&&fuelCalculate){verCond=false;if(econetVer!=undefined&&econetVer!=null){var econetVerArr=econetVer.split('.')
if(econetVerArr.length>2&&parseInt(econetVerArr[2])>3500){verCond=true;}}
if(verCond&&regParams!=undefined&&regParams!=null&&controller.type_!=ECOMAX_850i_TYPE&&Object.keys(regParams).indexOf("fuelConsum")!=-1){$('#tabHrEmFuelConsum').show()}else{$('#tabHrEmFuelConsum').hide()}}else{$('#tabHrEmFuelConsum').hide()}}
function parseServerDate(str){var digitpattern=/\d+/g;var matches=str.match(digitpattern);var milliseconds=matches[6]==undefined?0:matches[6];var date=new XDate(matches[0],matches[1]-1,matches[2],matches[3],matches[4],matches[5],milliseconds/1000,true);return date;}
function pad(number){var r=String(number);if(r.length===1){r='0'+r;}
return r;}
function toISOString(date){return date.getFullYear()
+'-'+pad(date.getMonth()+1)
+'-'+pad(date.getDate())
+'T'+pad(date.getHours())
+':'+pad(date.getMinutes())
+':'+pad(date.getSeconds())
+'.'+String((date.getMilliseconds()/1000).toFixed(3)).slice(2,5)
+'Z';}
function toUTC(date){var diff=date.getTimezoneOffset();date.setMinutes(date.getMinutes()+diff);return date;}
function convertUTCISOTime2LocalString(dateStr){return parseServerDate(dateStr).toLocaleString();}
function doStart(load_devices=true){createLanguagesPopup();$("#ecoNetScrTitles").removeClass('devSectionTitle');$('#logoEconetPlum').show();updater.doUpdate();$('.selectricEconetCtrl').selectric('refresh');if(isMemberOfGroup(GROUP_DEVICES)){$('#topNavScrTitle').text("")
$("#producersListArea").show();controller.getProducersList(completeProducersList);$("#deviceVersion_combobox").show();$("#verList").show();controller.getDevSoftVers(completeDevSoftVers);}else{if(isMemberOfGroup(GROUP_PRODUCER)){controller.getUserProducersList(resultProducersList);}else{$("#producersListArea").hide();}
$("#deviceVersion_combobox").hide();$("#verList").hide();}
loadLangFromCookie();if(load_devices){controller.getDevices(createDevicesTable,devices_active,devices_notactive,devices_blocked,devices_deviceType,devices_uid,devices_prodId,devices_current_page,devices_softVer,$('#devfilter_ver_mod_a').val(),$('#devfilter_ver_panel').val());}
initTabs();ngd_hist.init_elements();}
function initTabs(){if(isNotAnonymous()){$('#logoEconetPlum').show();}}
function checkCurrentDevActive(){return(typeof devices_dict!=='undefined')&&(typeof updater.currentDevice_!=='undefined')&&devices_dict[updater.currentDevice_].state!=STATE_NOT_ACTIVE;}
function checkCurrentDevBlocked(){console.log(devices_dict[updater.currentDevice_]);return(typeof devices_dict!=='undefined')&&(typeof updater.currentDevice_!=='undefined')&&devices_dict[updater.currentDevice_].state==STATE_BLOCKED;}
function setRemoteMenuCurrentLanguage(){if(remote_menu_languages!=null){remote_menu_current_language_version='';remote_menu_default_language_version='';for(let i=0;i<remote_menu_languages.length;i+=1){let lang_element=remote_menu_languages[i]
if('default'in lang_element&&lang_element['default']){remoteMenuDefaultLang=lang_element['code']
remote_menu_default_language_version=lang_element['version']
if(remoteManuLang=="default"){remote_menu_current_language_version=lang_element['version']}}
if(remoteManuLang!="nosel"){if(remoteManuLang!="default"){if(lang_element['code']==remoteManuLang){remote_menu_current_language_version=lang_element['version']}}}else{if(lang_element['code'].toLowerCase()==currLang){remote_menu_current_language_version=lang_element['version']}}}
if(remote_menu_current_language_version.length==0){remote_menu_current_language_version=remote_menu_default_language_version;}}}
function getRemoteMenuLangListResponse(result,textStatus,xmlhttprequest){if(result!=null&&result.data!=null&&result.data.length>0){remote_menu_languages=result.data;setRemoteMenuCurrentLanguage();updater.remoteMenuVer_[REMOTE_MENU_PARAMS_LANGS_]=result.remoteMenuLangsVer;updater.reloadRemoteMenuTexts();}}
function reloadRemoteMenuData(){if(currLangcodeInLangList()){updater.controller_.getRemoteMenuParamsNames(getRemoteMenuParamsNamesResponse);updater.controller_.getRemoteMenuCatsNames(getRemoteMenuCatsNamesResponse);updater.controller_.getRemoteMenuParamsUnitsNames(getRemoteMenuParamsUnitsNamesResponse);updater.controller_.getRemoteMenuParamsEnums(getRemoteMenuParamsEnumsResponse);updater.controller_.getRemoteMenuCurrDataDisp(getRemoteMenuCurrDataDispResponse);updater.controller_.getRemoteMenuLocksNames(getRemoteMenuLocksNamesResponse);updater.controller_.getRemoteMenuAlarmsNames(getRemoteMenuAlarmsNamesResponse);}}
function drawSignalQuality(quality){if(controller.only_device){}else{var canvas=$('#cvsNetworkQuality')[0];var context=canvas.getContext("2d");context.clearRect(0,0,canvas.width,canvas.height);var colWidth=Math.floor(canvas.width/5.5);var colWithSpace=Math.floor(colWidth*1.5);context.fillStyle="#2f323b";var maxColumns=4.0;var columnRange=100.0/maxColumns;var currSignal=Math.ceil(quality/columnRange);for(var i=0;i<currSignal;++i){context.beginPath();context.rect(i*colWithSpace,canvas.height*(0.25*(maxColumns-i-1)),colWidth,canvas.height);context.fill();}}}
function wifiInfoRefresh(quality,strength){var show_panel=false;if(quality!=undefined){$('#lbRegWifiQualValue').html(quality+"%")
drawSignalQuality(quality)
$('#wifiQualRow').show()
show_panel=true;}else{$('#wifiQualRow').hide()}
if(strength!=undefined){$('#lbRegWifiStrengthValue').html(strength+" dBm")
$('#wifiStrengthRow').show()
show_panel=true;}else{$('#wifiStrengthRow').hide()}
if(show_panel)
$('#wifiInfoPanel').show()
else
$('#wifiInfoPanel').hide()}