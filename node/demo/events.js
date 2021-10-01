const EventEmitter = require('events')

let emitter = new EventEmitter()

emitter.on('anything', data => {
    console.log('ON: anything', data)
})

emitter.emit('anything',{a:1})
emitter.emit('anything',{b:2})