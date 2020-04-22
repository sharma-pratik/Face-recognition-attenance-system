import 'dart:convert';
import 'HomePage.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_spinkit/flutter_spinkit.dart';

class UserLoginHome extends StatefulWidget {
  UserLoginHome({Key key}) : super(key: key);

  @override
  _UserLoginHomeState createState() => _UserLoginHomeState();
}

class _UserLoginHomeState extends State<UserLoginHome> {

  // variables
  var dropdownValue;
  bool isButtonDisabled = false;
  GlobalKey<FormState> _globalKey  = new GlobalKey();
  String validEmailValue, validPWDValue;
  var postEmailError = null;
  var postPasswordError = null;
  bool isDropDownErrorEnable = false;
  String postDropDownError = "";
  var session_id = null;
  Future<SharedPreferences> _prefs = SharedPreferences.getInstance();
  Future<String> userData;
  var _activeObscureIcon = Image.asset("assets/visible_eye.png", width: 25, height: 25,);
  var _obscureText = true;
  var csrfTokenValue = null;

  @override
  void initState() {

      super.initState();
      
      if(session_id != null){
    
        // checking if session is not expire
          httpRequester(csrfTokenValue =true).then((value){

            setState(() {
              csrfTokenValue = value['csrf_token'];
            });

            httpRequester().then((resp){
                int statusCode = resp["status_code"];
                
                // redirect user to Home Page
                if(statusCode==208){
                  print("already logged in");
                  Navigator.push(context, MaterialPageRoute(builder: (context) => HomePage()));
                  
                }
                else if (statusCode ==400){
                  print("bad reqeust. Expire");
                }
                else {
                  print("unknown error $statusCode");
                }
            }).catchError((onError){
              print("error $onError");
            });
          }).catchError((onError){
              print("error $onError");
          });
      }
      else{
        // First time opening the app
        print("sesssion id is empty $session_id");
      }
  }

  Future<Map> httpRequester([csrfTOkenFetch=true]) async {

    Map<String, dynamic> data = {};
    print("fetch token $csrfTOkenFetch");
    if (csrfTOkenFetch){
      
      String csrfTokenUrl = "http://192.168.1.100:8000/api/get_csrf_token";
      
      var httpResp =  await http.get(
                          Uri.encodeFull(csrfTokenUrl),
                          headers: {"accept":"text/html"}
                      );
      print(httpResp);
      data['csrf_token']= httpResp.body;
    }
    else{

        print("session id $session_id");
        String loginUrl = "http://192.168.1.100:8000/api/user/login";
        var headers = <String,String>{};
        var userInputData = {};

        userInputData["user_type"] = dropdownValue;
        userInputData["email"] = validEmailValue;
        userInputData["password"] = validPWDValue;

        headers["accept"] = "application/json";
        headers["Content-Type"] = "application/json";
        headers["X-CSRFToken"] = csrfTokenValue;
        if(session_id !=null) headers["Cookie"] = "csrftoken:$csrfTokenValue;session_id:$session_id";
        
        var httpResp =  await http.post(
                            Uri.encodeFull(loginUrl),
                            body: jsonEncode(userInputData),
                            headers: headers
                        );
        data["status_code"] = httpResp.statusCode;
        data["data"] = json.decode(json.decode(httpResp.body));
    }
    print(data);
    return data;
  }

  // validate email
  String validateEmail(String inputEmailValue, [bool emailResp]){

    String regPattern = r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}";
    RegExp regExp = new RegExp(regPattern);

    if( postEmailError == null){
        if(inputEmailValue.isNotEmpty){
            if (regExp.hasMatch(inputEmailValue)){
                  return null;
              }
            return "Email format not valid";
          }
        return "Email can not be empty";
      }
      return postEmailError;
  }

  // validate password
  String validatePwd(inputPwdValue){

      if(postPasswordError==null){
          if(inputPwdValue.isNotEmpty){
            return null;
          }
        return "Password can not be empty";
      }
      return postPasswordError;
  }

  // method for changing pwd field icons
  void changePasswordView(){

    setState(() {
      _obscureText = ! _obscureText;

      if (_obscureText){
        _activeObscureIcon = Image.asset("assets/visible_eye.png", width: 25, height: 25,);
      }
      else{
        _activeObscureIcon = Image.asset("assets/hide_eye.png", width: 25, height: 25,);
      }
    });
  }

  // cleaning values
  void _cleanAllValues(){
    setState(() {
      postEmailError = null;
      postDropDownError = "";
      postPasswordError = null;
      isDropDownErrorEnable = false;
    });
  }

  // set value in shared preferences
  Future<void> setSPValues(data) async{
    print("in setspvalues");
    final SharedPreferences prefs = await _prefs;
      setState(() {

          session_id = data["data"]['session_id'];
          var encodeUserData = json.encode(data["data"]['user_data']);

          prefs.setString('sp_user_data', encodeUserData);
          print(prefs.getString('sp_user_data'));
      });
  }



  // Login button cicked
  void _userLoginTasks() async{

    setState(() {
      isButtonDisabled = true;
    });

      _cleanAllValues();
      // validating user form input values
      if(_globalKey.currentState.validate()){
          print("all fields are valid");
          _globalKey.currentState.save();

          await httpRequester(true).then((response) async {

              setState(() {
                  csrfTokenValue = response['csrf_token'];
                  print("fetching csrf $csrfTokenValue");
              });

             await httpRequester(false).then((response) async{
                  
                  print("response is $response");
                  int statusCode = response["status_code"];

                  // 202
                  if (statusCode==202){
                    
                    await setSPValues(response["data"]);
                    setState(() {
                      isButtonDisabled = false;
                    });
                    Navigator.push(context, MaterialPageRoute(builder: (context) => HomePage()));
                  }

                  // 400
                  else if( statusCode==400){
                  
                    print("invalid user type");
                    setState(() {
                      postDropDownError = response["data"]["data"];
                      isDropDownErrorEnable = true;
                    });
                    _globalKey.currentState.validate();
                  }

                  // 401
                  else if(statusCode == 401){

                      if (response['data']['data']['email'].isNotEmpty){

                          setState(() {
                              postEmailError = response['data']['data']['email'];
                          });
                      }
                    else if (response['data']['data']['password'].isNotEmpty){
                        
                        setState(() {
                          postPasswordError =  response['data']['data']['password'];
                        });
                    }

                    _globalKey.currentState.validate();
                  }
                  //
              }).catchError((onError){
              print("error $onError");
            });
          }).catchError((onError){

              print(onError); 
              // show pop to user
              if(onError.toString().contains("SocketException:")){
                print("Please check your interent connection");
              }
            });
        }
        else{
          print("form field are invalid");
          print(postEmailError);
        }
      print("make button again avaialble");
      setState(() {
        isButtonDisabled = false;
      });
  }




  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      body: userLoginBody(context),
    );
  }

  // loading icon
  final spinkit = SpinKitThreeBounce(
     color: Colors.black,
     size: 15.0,
  );

  // User login view
  Widget userLoginBody([context]){
    
    return new
              Container(
                  decoration: BoxDecoration(
                      image: const DecorationImage(
                          fit: BoxFit.cover,
                          image: AssetImage("assets/login_bg_image4.png")
                      ),
                  ),
                  child:
                      Form(
                          key: _globalKey,
                          autovalidate: false,
                          child: new 
                                    ListView(
                                        children: <Widget>[
                                            Container(
                                              child: new RichText(
                                                  textAlign: TextAlign.center,
                                                  text: TextSpan(
                                                      children:<TextSpan> [
                                                          TextSpan(text: "LOG", style: TextStyle(color: Colors.white,height:5, fontSize: 50 )),
                                                          TextSpan(text: "IN", style: TextStyle(color: Colors.greenAccent, height:5, fontSize: 50 )),
                                                      ]
                                                  )
                                              ),
                                            ),
                                            Container(
                                                decoration: BoxDecoration(
                                                  border: Border.all(width: 2, color:Color(0xff343434)),
                                                  borderRadius: BorderRadius.circular(12)
                                                ),
                                                margin: EdgeInsets.fromLTRB(20, 10, 20, 10),  
                                                padding: EdgeInsets.fromLTRB(10, 5, 10, 5),
                                                child :
                                                    Column(
                                                        children:
                                                            <Widget>[
                                                                new Row(
                                                                    children: <Widget>[
                                                                            new Container(
                                                                                  child: Icon(Icons.supervised_user_circle, size: 21, color: Colors.white,)
                                                                                ),
                                                                            new Expanded(
                                                                                    // margin: EdgeInsets.fromLTRB(0, 0, 0, 0),
                                                                                    child:
                                                                                        new DropdownButtonHideUnderline(
                                                                                          
                                                                                            child:new ButtonTheme(
                                                                                                alignedDropdown: true,
                                                                                                child: DropdownButton(
                                                                                                  items: ['HOD','STUDENT', 'ADMIN', 'MANAGEMENT', 'ASSISTANCE PROFESSOR']
                                                                                                      .map<DropdownMenuItem<String>>((String value) {
                                                                                                      return DropdownMenuItem<String>(
                                                                                                          value: value,
                                                                                                          child: Center(child:Text(value, style: TextStyle(color: Colors.white, fontSize: 15)),)
                                                                                                        );
                                                                                                      })
                                                                                                    .toList(),
                                                                                                  
                                                                                                  onChanged: (newValue) {
                                                                                                    setState(() {
                                                                                                      dropdownValue = newValue;
                                                                                                    });
                                                                                                  },
                                                                                                  value:dropdownValue,
                                                                                                  isExpanded: false,
                                                                                                  style: TextStyle(fontSize: 15.0),
                                                                                                  hint: Text("Choose User type", style: TextStyle(color: Colors.white),),
                                                                                                )
                                                                                            )
                                                                                        )
                                                                                )
                                                                    ],
                                                                ),
                                                                new Center(
                                                                  child: isDropDownErrorEnable ? new Text(postDropDownError, style: TextStyle(color: Colors.red, fontSize: 10),) : null,
                                                                )
                                                            ],
                                                    ),
                                            ),
                                            Container(
                                                decoration: BoxDecoration(
                                                    border: Border.all(width: 2, color:Color(0xff343434)),
                                                    borderRadius: BorderRadius.circular(12)
                                                  ),
                                                margin: EdgeInsets.fromLTRB(20, 10, 20, 10),  
                                                padding: EdgeInsets.fromLTRB(10, 5, 10, 5),
                                                child: new TextFormField(
                                                    validator: validateEmail,
                                                    onSaved: (value){
                                                      validEmailValue = value.trim();
                                                    },
                                                    style: TextStyle(color: Colors.white, fontSize: 15),
                                                    decoration : new InputDecoration(
                                                        border: InputBorder.none,
                                                        icon: new Container(
                                                          child:Image.asset("assets/email_icon.png", width: 20, height: 20,),
                                                        ),
                                                          hintText: "Email address",  
                                                        hintStyle: TextStyle(color: Colors.white, fontSize: 15)
                                                    )   
                                                ),
                                            ),
                                            Container(
                                                decoration: BoxDecoration(
                                                    border: Border.all(width: 2, color:Color(0xff343434)),
                                                    borderRadius: BorderRadius.circular(12)
                                                  ),
                                                margin: EdgeInsets.fromLTRB(20, 10, 20, 10),  
                                                padding: EdgeInsets.fromLTRB(10, 5, 10, 5),
                                                child: Row(
                                                    children: <Widget>[
                                                        new Expanded(
                                                            flex: 90,
                                                            child: TextFormField(
                                                                obscureText: _obscureText,
                                                                validator: validatePwd,
                                                                onSaved: (value){
                                                                    validPWDValue= value.trim();
                                                                },
                                                                style: TextStyle(color: Colors.white, fontSize: 15),
                                                                decoration : new InputDecoration(
                                                                    border: InputBorder.none,
                                                                    icon: new Container(child:Image.asset("assets/pwd_icon.png", width: 20, height: 20,)),
                                                                    hintText: "password",
                                                                    hintStyle: TextStyle(color: Colors.white, fontSize: 15)
                                                                )   
                                                            ),
                                                        ),
                                                        new Expanded(
                                                          child: IconButton(icon: _activeObscureIcon, onPressed: changePasswordView, ),
                                                          flex: 10,
                                                        )
                                                    ],
                                                ),
                                            ),
                                            Container(
                                                margin: EdgeInsets.fromLTRB(40, 50, 40, 10),
                                                height: 65,
                                                color: isButtonDisabled ? Color(0xff9A9696) : Color(0xff28D8A1),
                                                child: new MaterialButton(
                                                    splashColor: Colors.red,
                                                    onPressed: isButtonDisabled ? null : _userLoginTasks,
                                                    child: isButtonDisabled  ? spinkit : new Text("LOGIN", style: TextStyle(color: Colors.white, fontSize: 15),),
                                                ),
                                            ),
                                            Container(
                                                margin: EdgeInsets.fromLTRB(60, 10, 60, 10),
                                                child:
                                                    new Row(
                                                        mainAxisAlignment: MainAxisAlignment.center,
                                                        children: <Widget>[
                                                            new Text("Forgot password ?", style: TextStyle(color: Colors.white, fontSize: 10),),
                                                            new FlatButton(onPressed: null, padding: EdgeInsets.all(0),child: new Text(" Recover here", style: TextStyle(color: Color(0xff28D8A1), fontSize: 10),))
                                                        ],
                                                    ),
                                            )
                                        ],
                                    ),
                              ),
                );
  }
}