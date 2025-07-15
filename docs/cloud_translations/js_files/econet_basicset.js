function getLanguages(){return["pl","en","de","fr","uk","da","cz","it","ro","bg","tr","es","hr","hu","sk","sr","lv","nl","ru"];}
function initFlag(){$('#flags').empty();$('#flags').append('<label>'+currLang+'</label>');$('#flags').append('<div class="imgLang lang_'+currLang+'" ></div>');}
function openLangPopup(){var div=$('#chooseLangPopup');if(div.is(':visible')){div.hide();}else{div.show();}}
function createLanguagesPopup(){$('#chooseLangPopupContent').empty();var init_languages=getLanguages();for(l in init_languages){$('#chooseLangPopupContent').append('<div class="imgLang lang_'
+init_languages[l]
+'" onclick="setLanguage(event,\''
+init_languages[l]+'\')" ></div>');}}
function startLoginForm(){initFlag();createLanguagesPopup();loadLangFromCookie();hidePreloader();showCookiesInfo();$('#loginMain').show();}
function customizeRegistrationForm(){translateErrors();showRegulatorAddresForm(!$("#id_regAddress").prop("checked"));$('.selectricEconetCtrl').selectric('refresh');$('#id_serviceAccess').selectric('refresh');}
function showRegulatorAddresForm(show){if(show){$('#rowRegStreet').show();$('#rowRegPostalCode').show();$('#rowRegCountry').show();$('#rowRegHouse').show();$('#rowApartm').show();$('#rowRegCity').show();}else{$('#rowRegStreet').hide();$('#rowRegPostalCode').hide();$('#rowRegCountry').hide();$('#rowRegHouse').hide();$('#rowApartm').hide();$('#rowRegCity').hide();}}
function showPreloader(){if($('#deviceLeftPanelNavArea').is(':visible')&&!$('#aMenu').is(':visible')||$('#adminLeftPanel').is(':visible')){$('#preloader').attr("class","preloaderLM");}else{$('#preloader').attr("class","preloaderCenter");}
$('#preloader').show();}
function hidePreloader(){$('#preloader').hide();}
function showCookiesInfo(){if(Cookies.get("ecoSrvCookies")==undefined){$('#cookiesAcceptance').show();}}
function acceptCookies(){Cookies.set("ecoSrvCookies","true",{expires:new Date(9999,12,31,23,59,59)});$('#cookiesAcceptance').hide();}
function translateCookiesPolicy(){$('#cookTitle').text(translate("cookTitle"));if(window.gl_const!==undefined){$('#cookSubtitle').text(translate("termsSubtitle").replace("{$service}",gl_const.service).replace("{$domain}",gl_const.domain));}
$('#cooPolicy').empty();var key=currLang;if(typeof polcookies!=='undefined'){if(polcookies!=undefined&&polcookies!=null&&polcookies[key]!=undefined){$('#cooPolicy').append(polcookies[key]);}
else{$('#cooPolicy').append(polcookies['en']);}}}
function acceptLogin(){$('#loginMain').hide();showPreloader();}
function checkAlerts(){controller.getAlertsDates(getAlertsDatesResponse);}
function getAlertsDatesResponse(result){if(!("date_added"in result))
{$('#alertsBtn').hide();return;}
var now=new Date();var dateNow=new Date(now.getTime()+now.getTimezoneOffset()*60000);dateNow=js_yyyy_mm_dd_hh_mm_ss(dateNow);dateNow=dateNow.concat("+00:00");alertText="";if(result["date_user"]!="None"){var userDate=new Date(result["date_user"].replace(" ","T"));}else{var userDate=result["date_user"];}
var dateAdded=new Date(result["date_added"].replace(" ","T"));var fromDate=new Date(result["date_from"].replace(" ","T"));var toDate=new Date(result["date_to"].replace(" ","T"));if(now>toDate){$('#alertsBtn').hide();}
else{Text=prepareAlertText(fromDate,toDate);$('#alertsBtn').show();$('#alertText').text(Text);if(userDate=="None"||userDate<dateAdded){$('#alertBar').show();$("#alertsBtn").addClass("alertsBtnClicked");controller.saveAlertDateUser(dateNow);}}
return;}
function showAlerts(){$("#alertBar").slideToggle("fast",function(){if($('#alertBar').is(':visible')){$("#alertsBtn").addClass("alertsBtnClicked");}else{$("#alertsBtn").removeClass("alertsBtnClicked");}});}
function prepareAlertText(fromDate,toDate){var alertText=translate("alertText");alertText=alertText.replace("==/fromDateTime/==",prepareDate(fromDate));alertText=alertText.replace("==/toDateTime/==",prepareDate(toDate));return alertText;}
function addZero(val){if(val<10){val="0"+val;}
return val;}
function prepareDate(date){var year=date.getFullYear();var month=addZero(date.getMonth()+1);var day=addZero(date.getDate());var hours=addZero(date.getHours());var minutes=addZero(date.getMinutes());var dateString=year+"."+month+"."+day+" "+hours+":"+minutes;return dateString;}
function js_yyyy_mm_dd_hh_mm_ss(date){year=""+date.getFullYear();month=""+(date.getMonth()+1);if(month.length==1){month="0"+month;}
day=""+date.getDate();if(day.length==1){day="0"+day;}
hour=""+date.getHours();if(hour.length==1){hour="0"+hour;}
minute=""+date.getMinutes();if(minute.length==1){minute="0"+minute;}
second=""+date.getSeconds();if(second.length==1){second="0"+second;}
return year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second;}
function hideAlertBar(){$('#alertBar').hide();$("#alertsBtn").removeClass("alertsBtnClicked");}
function ResultLabel(labelObject){this.label_=labelObject;this.showTimeout_=5000;this.showError=function(message){this.label_.attr('class','errLabel');this.label_.text(message);this.label_.show();this.clearLabel();};this.showInfo=function(message){this.label_.attr('class','infoLabel');this.label_.text(message);this.label_.show();this.clearLabel();};this.clearLabel=function(){var self=this;setTimeout(function(){self.label_.text('');},this.showTimeout_);};}/*!
 * Cookies.js - 0.4.0
 *
 * Copyright (c) 2014, Scott Hamper
 * Licensed under the MIT license,
 * http://www.opensource.org/licenses/MIT
 */

(function(undefined){'use strict';var Cookies=function(key,value,options){return arguments.length===1?Cookies.get(key):Cookies.set(key,value,options);};Cookies._document=document;Cookies._navigator=navigator;Cookies.defaults={path:'/'};Cookies.get=function(key){if(Cookies._cachedDocumentCookie!==Cookies._document.cookie){Cookies._renewCache();}
return Cookies._cache[key];};Cookies.set=function(key,value,options){options=Cookies._getExtendedOptions(options);options.expires=Cookies._getExpiresDate(value===undefined?-1:options.expires);Cookies._document.cookie=Cookies._generateCookieString(key,value,options);return Cookies;};Cookies.expire=function(key,options){return Cookies.set(key,undefined,options);};Cookies._getExtendedOptions=function(options){return{path:options&&options.path||Cookies.defaults.path,domain:options&&options.domain||Cookies.defaults.domain,expires:options&&options.expires||Cookies.defaults.expires,secure:options&&options.secure!==undefined?options.secure:Cookies.defaults.secure};};Cookies._isValidDate=function(date){return Object.prototype.toString.call(date)==='[object Date]'&&!isNaN(date.getTime());};Cookies._getExpiresDate=function(expires,now){now=now||new Date();switch(typeof expires){case'number':expires=new Date(now.getTime()+expires*1000);break;case'string':expires=new Date(expires);break;}
if(expires&&!Cookies._isValidDate(expires)){throw new Error('`expires` parameter cannot be converted to a valid Date instance');}
return expires;};Cookies._generateCookieString=function(key,value,options){key=key.replace(/[^#$&+\^`|]/g,encodeURIComponent);key=key.replace(/\(/g,'%28').replace(/\)/g,'%29');value=(value+'').replace(/[^!#$&-+\--:<-\[\]-~]/g,encodeURIComponent);options=options||{};var cookieString=key+'='+value;cookieString+=options.path?';path='+options.path:'';cookieString+=options.domain?';domain='+options.domain:'';cookieString+=options.expires?';expires='+options.expires.toUTCString():'';cookieString+=options.secure?';secure':'';return cookieString;};Cookies._getCookieObjectFromString=function(documentCookie){var cookieObject={};var cookiesArray=documentCookie?documentCookie.split('; '):[];for(var i=0;i<cookiesArray.length;i++){var cookieKvp=Cookies._getKeyValuePairFromCookieString(cookiesArray[i]);if(cookieObject[cookieKvp.key]===undefined){cookieObject[cookieKvp.key]=cookieKvp.value;}}
return cookieObject;};Cookies._getKeyValuePairFromCookieString=function(cookieString){var separatorIndex=cookieString.indexOf('=');separatorIndex=separatorIndex<0?cookieString.length:separatorIndex;return{key:decodeURIComponent(cookieString.substr(0,separatorIndex)),value:decodeURIComponent(cookieString.substr(separatorIndex+1))};};Cookies._renewCache=function(){Cookies._cache=Cookies._getCookieObjectFromString(Cookies._document.cookie);Cookies._cachedDocumentCookie=Cookies._document.cookie;};Cookies._areEnabled=function(){var testKey='cookies.js';var areEnabled=Cookies.set(testKey,1).get(testKey)==='1';Cookies.expire(testKey);return areEnabled;};Cookies.enabled=Cookies._areEnabled();if(typeof define==='function'&&define.amd){define(function(){return Cookies;});}else if(typeof exports!=='undefined'){if(typeof module!=='undefined'&&module.exports){exports=module.exports=Cookies;}
exports.Cookies=Cookies;}else{window.Cookies=Cookies;}})();