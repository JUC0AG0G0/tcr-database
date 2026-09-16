import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToMany } from 'typeorm';
import type { Relation } from 'typeorm';
import { Championship } from './championship.entity.js';
import { Event } from './event.entity.js';
import { Standing } from './standing.entity.js';

@Entity('seasons')
export class Season {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int' })
  year: number;

  @ManyToOne(() => Championship, championship => championship.seasons)
  championship: Relation<Championship>;

  @OneToMany(() => Event, event => event.season)
  events: Relation<Event>[];

  @OneToMany(() => Standing, standing => standing.season)
  standings: Relation<Standing>[];
}