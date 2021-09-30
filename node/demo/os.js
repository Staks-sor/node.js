const os = require('os')
const chalk = require('chalk')

console.log(chalk.red('Операционаая система: ', os.platform()))

console.log(chalk.green('Архитектура процессора: ', os.arch()))

console.log('Информация по процессорам: ', os.cpus())

console.log(chalk.blue('Свободная память: ', os.freemem()))

console.log(chalk.blue('Всего памяти: ', os.totalmem()))

console.log(chalk.red('домашняя директория: ', os.homedir()))