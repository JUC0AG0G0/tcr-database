import { DataSource } from 'typeorm';
import { config } from 'dotenv';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

// Recréation de __dirname pour le monde ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

config({ path: '../.env' });

export const AppDataSource = new DataSource({
  type: 'postgres',
  url: process.env.DATABASE_URL,
  entities: [__dirname + '/**/*.entity{.ts,.js}'],
  migrations: [__dirname + '/migrations/*{.ts,.js}'],
  synchronize: false,
});