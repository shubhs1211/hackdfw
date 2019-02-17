var express = require('express');
var path = require('path');
var rp = require('request-promise');

const app = express()
const port = 3000

app.use('/routes', express.static('routes'))
app.get('/', (req, res) => res.sendFile(path.join(__dirname + '/Hello.html')));
app.get('/alexa',function(req,res){
  
  rp('https://82622bb2.ngrok.io').then(body => {
    console.log(body);
    body = JSON.parse(body);
    if(body["current_state"]=="init"){
      console.log(body["current_state"]);
      res.send({obj:"box"});
      }
    if(body["current_state"]=="car"){
      res.send({obj:"car"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="house"){
      res.send({obj:"house"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="home"){
      res.send({obj:"house"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="loan"){
      res.send({obj:"loan"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="insurance"){
      res.send({obj:"insurance"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="age"){
      res.send({obj:"age"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="loan_term"){
      res.send({obj:"clock"});
      console.log(body["current_state"]);
    }
    if(body["current_state"]=="exp"){
      res.send({obj:"clock"});
      console.log(body["current_state"]);
    }
    else
    {
      res.send({obj:"box"});
      console.log(body["current_state"]);
  }}).catch(err => {
      console.log(err);
  });

});

app.listen(port, () => console.log(`Example app listening on port ${port}!`));

