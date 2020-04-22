
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  HomePage({Key key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  // variables

  Future<SharedPreferences> _prefs = SharedPreferences.getInstance();
  Map<String, dynamic> userData = {};
  Future<Map<String, dynamic>> userDataInStringFormat;
  String email = "";
  String branch;
  var user_data;

  @override
  void initState() { 
    super.initState();

    print("in initstate");
      _prefs.then((SharedPreferences preferences){
        
        var d = json.decode(preferences.getString("sp_user_data"));
        userData = d;
        email = userData["email"];
        print("In initstate $email");
    });
    print(email);
  }

 
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title:Text("Welcome bar")),
      body: homePageBody(),
    );
  }
   Widget homePageBody(){
    return Container(
      child: new Column(
        children: <Widget>[
          new Text("Welcome", style: TextStyle(color: Colors.white),),
          new Text(email, style: TextStyle(color: Colors.white),),
        ],
      ),
    );
  }
}