const path = require('path')
const chalk = require('chalk')

console.log(chalk.blue('Название фаила: ', path.basename(__filename)))

console.log(chalk.yellow('Имя директории: ', path.dirname(__filename)))

console.log(chalk.red('Расширение файла: ', path.extname(__filename)))

console.log('Parse: ', path.parse(__filename).name)