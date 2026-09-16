import { Entity, PrimaryGeneratedColumn, Column, ManyToOne } from 'typeorm';
import type { Relation } from 'typeorm';
import { Season } from './season.entity.js';
import { Driver } from './driver.entity.js';

@Entity('standings')
export class Standing {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int' })
  position: number;

  @Column({ type: 'float' })
  points: number;

  @ManyToOne(() => Season, season => season.standings)
  season: Relation<Season>;

  @ManyToOne(() => Driver, driver => driver.standings)
  driver: Relation<Driver>;
}