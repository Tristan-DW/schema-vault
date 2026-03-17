#!/usr/bin/env node
const { Command } = require('commander');
const { init } = require('./commands/init');
const { create } = require('./commands/create');
const { up } = require('./commands/up');
const { down } = require('./commands/down');
const { status } = require('./commands/status');

const program = new Command();

program
  .name('sv')
  .description('schema-vault - database migration CLI')
  .version('1.0.0');

program
  .command('init [name]')
  .description('Initialize a new schema-vault project')
  .action(init);

program
  .command('create <name>')
  .description('Create a new migration file')
  .action(create);

program
  .command('up')
  .description('Apply pending migrations')
  .option('--dry-run', 'Preview SQL without executing')
  .action(up);

program
  .command('down')
  .description('Roll back migrations')
  .option('--steps <n>', 'Number of migrations to roll back', '1')
  .action(down);

program
  .command('status')
  .description('Show migration status')
  .action(status);

program.parse();
