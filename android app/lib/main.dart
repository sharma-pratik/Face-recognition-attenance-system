import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui';
import 'dart:async';
import 'package:dropdown_formfield/dropdown_formfield.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'routes/UserLoginHome.dart';

void main() => runApp(new FaceDetectionApp());


class FaceDetectionApp extends StatelessWidget {
  const FaceDetectionApp({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {

      return new MaterialApp(
          theme: new ThemeData( canvasColor: Color(0xff343434)),
          home: UserLoginHome()
      );
    }
}


// Saffold widget for containing login form
// class LoginHome extends StatefulWidget {
//   LoginHome({Key key}) : super(key: key);

//   @override
//   _LoginHomeState createState() => _LoginHomeState();
// }

// class _LoginHomeState extends State<LoginHome> {

// //  password input fields variables


// @override
//   void initState() {
//     // TODO: implement initState
//     super.initState();
//     userData = _prefs.then((SharedPreferences prefs){
//       return (prefs.getString('sf_user_data')?? "");
//     });
//     print("value of session $session_id");
//     print("value of share prefences $userData");
//   }

// // method for changing pwd field icons
//   void changePasswordView(){
    
//     setState(() {
//       _obscureText = ! _obscureText;

//       if (_obscureText){
//         _activeObscureIcon = Image.asset("assets/visible_eye.png");
//       }
//       else{
//         _activeObscureIcon = Image.asset("assets/hide_eye.png");
//       }
//     });
//   }

//   void _cleanAllValues(){
//     setState(() {
//       postEmailError = null;
//       postDropDownError = "";
//       postPasswordError = null;
//     });
//   }

//   // User login 
//   void _userLoginTaks() async{
//       SharedPreferences preferences = await SharedPreferences.getInstance();
//       String data = preferences.getString('sf_user_data');
//       print("login clicked $postEmailError and $data and session id $session_id");
//       _cleanAllValues();


//       if(_globalKey.currentState.validate()){
//         print("all fields are valid");
//         _globalKey.currentState.save();

//           // fetching csrf token
//           Future<String> fetchCsrfToken() async {
//               var response = await http.get(
               
//               );
//               return response.body;
//           }

//           // checking valid response 
//           fetchCsrfToken().then(
//             (successResp){

//               String csrfTokenValue = successResp;
//               var userData = {};
//               userData["user_type"] = dropdownValue;
//               userData["email"] = validEmailValue;
//               userData["password"] = validPWDValue;

//               Future<Map> authenticatingUser() async {
//                   var response = await http.post(
//                   Uri.encodeFull(loginUrl),
//                   body:jsonEncode(userData),
//                   headers: {
//                     "accept":"",
//                     "":csrfTokenValue,
//                     "Content-Type":"application/json",
//                   }
//                 );
                
//                 Map<String, dynamic> resp ={};
//                 resp["body"] = json.decode(json.decode(response.body));
//                 resp["status_code"] = response.statusCode;
//                 return resp;
//               }
//               // validating response
//               authenticatingUser().then(
//                 (resp){
//                   print(resp);

//                   if(resp['status_code']==401){

//                     if (resp['body']['data'][0]['email'].isNotEmpty){

//                       setState(() {
//                         postEmailError = resp['body']['data'][0]['email'];
//                         _globalKey.currentState.validate();
//                       });
//                     }
//                     else if (resp['body']['data']['password'] != null){
//                       setState(() {
//                         postPasswordError =  resp['body']['data']['password'];
//                         _globalKey.currentState.validate();
//                       });
//                     }
//                   }
//                   else if (resp['status_code']==400){
//                       setState(() {
//                       postDropDownError = resp['body']['data'];
//                     });
//                   }
//                   else if (resp['status_code']==202){
//                     setSPValues(resp['body']['data']);
//                   }
//                   else{
//                     print(resp['status_code']);
//                     print(resp['body']);
//                   }
//                   print("autovalide after making false $autoValidate");
//                 }
//               ).catchError((error){
//                 print("error is coming $error");
//               });
//             }
//           ).catchError(
//             (errorResp){
//               print("error is coming $errorResp");
//             }
//           );
//         }else{

//         }
//     }

//   // validate email
//   String validateEmail(String email, [bool emailResp]){
//     print("validating email");
//     String regPattern = r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}";
//     RegExp regExp = new RegExp(regPattern);

//     if( postEmailError == null){
//       if(email.isNotEmpty){
//         if (regExp.hasMatch(email)){
//               return null;
//           }
//         return "Email format not valid";
//       }
//       return "Email can not be empty";
//     }
//     return postEmailError;
//   }

//   // validate password
//   String validatePwd(value){
//     print("validating password");
//     if(postPasswordError==null){
//       if(value.isNotEmpty){
//         return null;
//       }
//       return "Password can not be empty";
//     }
//       return postPasswordError;
//   }


//   // set value in shared preferences

//   Future<void> setSPValues(data) async{

//     final SharedPreferences prefs = await _prefs;
//       setState(() {
//           session_id = data['session_id'];
//           var encodeUserData = json.encode(data['user_data']);
//           print(encodeUserData is String);
//           prefs.setString('sf_user_data', encodeUserData);
//           print(prefs.getString('sf_user_data'));
//       });
//   }

//   // variables
  

  
// }
