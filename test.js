/**
 * Created with PyCharm.
 * User: 4ikist
 * Date: 20.08.13
 * Time: 0:32
 * To change this template use File | Settings | File Templates.
 */
var request = require('request');

var obj = {
    session_id: 'lease1',
    identity: 'id',
    identity_type: 'email',
    app_name: 'test',
    status: 'ok',
    latency: 100,
    bytes_sent: 111,
    streaming_started_at: '2013-08-10 14:20:00',
    duration: 10,
    ticket: 100500,
    leased_at: '2013-08-10 14:20:00'
};

request.post('http://178.49.13.210:5000/sessions', {form: obj}, function (e, r, body) {
    console.log(body);
});