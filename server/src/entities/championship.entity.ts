import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import type { Relation } from 'typeorm';
import { Season } from './season.entity.js';

@Entity('championships')
export class Championship {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  region: string;

  @OneToMany(() => Season, season => season.championship)
  seasons: Relation<Season>[];
}