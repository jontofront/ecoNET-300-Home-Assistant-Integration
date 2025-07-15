// dev_set1.js - Controller Class and API Endpoint Definitions
// Source: https://www.econet24.com/static/ui/dev_set1.js?332fd073
// This file contains the main Controller class that handles all API communications

function logError(jqXHR,textStatus,errorThrown){
    console.log('Error! '+textStatus);
    console.log(errorThrown);
    console.log(jqXHR);
}

var ECOMAX_850P_TYPE=0;
var ECOMAX_850i_TYPE=1;

function Controller(destination,ecosrv_address){
    this.only_device=false;
    this.destination_=destination;
    this.ecosrvAddress_=ecosrv_address;
    this.protocol_type='';
    this.type_=0;
    
    this.setProtocolType=function(t){
        if(typeof t==="string"){
            this.protocol_type=t.toLowerCase();
        }
    };
    
    this.setType=function(t){
        if(typeof t==="number"){
            this.type_=t;
        }else{
            console.log("Warning: wrong type for Controller.setType()");
        }
    };
    
    // API Endpoint Methods
    
    this.getRemoteMenuLangs=function(responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmLangs?uid="+encodeURIComponent(updater.currentDevice_):"rmLangs"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getCurrentParamsEdits=function(responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmCurrentDataParamsEdits?uid="+encodeURIComponent(updater.currentDevice_):"rmCurrentDataParamsEdits"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuParamsNames=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmParamsNames?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmParamsNames"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuCatsNames=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmCatsNames?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmCatsNames"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuParamsUnitsNames=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmParamsUnitsNames?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmParamsUnitsNames"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuParamsEnums=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmParamsEnums?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmParamsEnums"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuLocksNames=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmLocksNames?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmLocksNames"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuStructure=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmStructure?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmStructure"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuCurrDataDisp=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmCurrentDataParams?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmCurrentDataParams"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuParamsData=function(responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmParamsData?uid="+encodeURIComponent(updater.currentDevice_):"rmParamsData"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuExistingLangsList=function(responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmExistingLangs?uid="+encodeURIComponent(updater.currentDevice_):"rmExistingLangs"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuAlarmsNames=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmAlarmsNames?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmAlarmsNames"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuParamsDescs=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmParamsDescs?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmParamsDescs"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    this.getRemoteMenuCatsDescs=function(responseMethod,lang){
        if(lang==null&&updater.currentDevice_){
            lang=getRmLang();
        }
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmCatsDescs?uid="+encodeURIComponent(updater.currentDevice_)+"&lang="+encodeURIComponent(lang):"rmCatsDescs"),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    // Authentication and Security Methods
    
    this.getPassword=function(responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"call/run/getServicePassword?uid="+encodeURIComponent(updater.currentDevice_):"password"),
            success:responseMethod,
            error:logError
        });
    };
    
    this.getETPassword=function(responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"getETservicePasswords?uid="+encodeURIComponent(updater.currentDevice_):"etpassword"),
            success:responseMethod,
            error:logError
        });
    };
    
    this.rmCheckAccess=function(password,responseMethod,errorMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmAccess?uid="+encodeURIComponent(updater.currentDevice_)+"&":"rmAccess?")+ "password="+encodeURIComponent(password),
            success:responseMethod,
            error:errorMethod
        });
        return false;
    };
    
    // Parameter Update Methods
    
    this.saveParam=function(name,value,responseMethod,errorMethod,bit){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"newParam?uid="+encodeURIComponent(updater.currentDevice_)+"&":"newParam?")+ "newParamName="+encodeURIComponent(name)+"&newParamValue="+encodeURIComponent(value),
            success:responseMethod,
            error:errorMethod
        });
        return false;
    };
    
    this.rmSaveParam=function(index,value,responseMethod,errorMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmNewParam?uid="+encodeURIComponent(updater.currentDevice_)+"&":"rmNewParam?")+ "newParamIndex="+encodeURIComponent(index)+"&newParamValue="+encodeURIComponent(value),
            success:responseMethod,
            error:errorMethod
        });
        return false;
    };
    
    this.rmSaveCurrParam=function(key,value,responseMethod,errorMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmCurrNewParam?uid="+encodeURIComponent(updater.currentDevice_)+"&":"rmCurrNewParam?")+ "newParamKey="+encodeURIComponent(key)+"&newParamValue="+encodeURIComponent(value),
            success:responseMethod,
            error:errorMethod
        });
        return false;
    };
    
    // Language and Settings Methods
    
    this.rmSaveLang=function(value,responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"rmSaveLang?uid="+encodeURIComponent(updater.currentDevice_)+"&":"rmSaveLang?")+ "lang="+encodeURIComponent(value),
            success:responseMethod,
            error:logError
        });
        return false;
    };
    
    // Software Update Methods
    
    this.updateSoftware=function(responseMethod,errorMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+(updater.currentDevice_?"updateEconet?uid="+updater.currentDevice_:"updateSoftware"),
            success:responseMethod,
            error:errorMethod
        });
    };
    
    // Device Management Methods
    
    this.getDevices=function(resultFunction,active,notactive,blocked,deviceType,uid,prodId,page,softVer,verModA,verPanel){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+"devices?active="+active+"&notactive="+notactive+"&blocked="+blocked+"&deviceType="+deviceType+"&uid="+uid+"&prodId="+prodId+"&page="+page+"&softVer="+softVer+"&verModA="+verModA+"&verPanel="+verPanel,
            success:resultFunction,
            error:logError
        });
    };
    
    // Device Settings Methods
    
    this.setDeviceSettings=function(uid,label,serviceAccess,alarmNotifications,responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+"setDeviceSettings?uid="+encodeURIComponent(uid)+"&label="+encodeURIComponent(label)+"&serviceAccess="+encodeURIComponent(serviceAccess)+"&alarmNotifications="+alarmNotifications,
            success:responseMethod,
            error:logError
        });
    };
    
    this.setDeviceAddressSettings=function(uid,street,house,apartment,postalCode,city,country,responseMethod){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+"setDeviceAddressSettings?uid="+encodeURIComponent(uid)+"&street="+encodeURIComponent(street)+"&house="+encodeURIComponent(house)+"&apartment="+encodeURIComponent(apartment)+"&postalCode="+encodeURIComponent(postalCode)+"&city="+encodeURIComponent(city)+"&country="+encodeURIComponent(country),
            success:responseMethod,
            error:logError
        });
    };
    
    // Key Management Methods
    
    this.updateKey=function(key,uid){
        $.ajax({
            type:"GET",
            dataType:'json',
            cache:false,
            url:this.destination_+"updateKey?key="+encodeURIComponent(key)+"&uid="+encodeURIComponent(uid),
            success:confirmUpdatingkKey,
            error:logError
        });
    };
}

// Additional utility functions and global variables would be here...
// (The file continues with many more functions, but this covers the main Controller class) 