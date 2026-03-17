const fs = require('fs');
const path = require('path');
const { loadConfig } = require('../config');
const { getDriver } = require('../drivers');
const chalk = require('chalk');

exports.up = async (options) => {
  const config = loadConfig();
  const driver = getDriver(config);

  await driver.ensureLockTable();

  const applied = await driver.getAppliedMigrations();
  const appliedSet = new Set(applied.map(m => m.name));

  const files = fs.readdirSync(config.migrationsDir)
    .filter(f => f.endsWith('.sql'))
    .sort();

  const pending = files.filter(f => !appliedSet.has(f));

  if (!pending.length) {
    console.log(chalk.green('Nothing to migrate - all up to date.'));
    return;
  }

  for (const file of pending) {
    const content = fs.readFileSync(path.join(config.migrationsDir, file), 'utf8');
    const upMatch = content.match(/-- up([\s\S]*?)(?:-- down|$)/);
    if (!upMatch) continue;

    const sql = upMatch[1].trim();

    if (options.dryRun) {
      console.log(chalk.cyan(`[dry-run] ${file}:`));
      console.log(chalk.gray(sql));
      continue;
    }

    try {
      await driver.execute(sql);
      await driver.recordMigration(file);
      console.log(chalk.green(`Applied: ${file}`));
    } catch (err) {
      console.error(chalk.red(`Failed: ${file}`), err.message);
      process.exit(1);
    }
  }
};
