const fs = require('fs')
const path = require('path')
const chalk = require('chalk')
//fs.mkdir(path.join(__dirname, 'test'), (err) => {
//    if (err) {
//        throw err
//    }
//        console.log(chalk.green('Папка создана'))
//})\

const filePath = path.join(__dirname, 'test', 'text.txt')

//fs.writeFile(filePath, 'Hello world!fuck', err => {
//    if (err) {
//        throw err
//    }
//    console.log('Фаил создан')
//    fs.appendFile(filePath, '\nHello again', err => {
//        if (err) {
//        throw err
//        }
//        console.log('Фаил создан')
//    })
//})

fs.readFile(filePath, 'utf8', (err, content) => {
    if (err) {
        throw err
    }
    console.log(content)
})