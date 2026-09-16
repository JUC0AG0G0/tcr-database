import { Entity, PrimaryGeneratedColumn, Column, ManyToOne } from 'typeorm';
import type { Relation } from 'typeorm';
import { Session } from './session.entity.js';
import { Driver } from './driver.entity.js';
import { Team } from './team.entity.js';
import { Car } from './car.entity.js';

@Entity('results')
export class Result {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int', nullable: true })
  startingPosition: number;

  @Column({ type: 'int', nullable: true })
  finishPosition: number;

  @Column({ nullable: true })
  status: string; // "Finished", "DNF", "DNS"

  @Column({ type: 'int', nullable: true })
  laps: number;

  @Column({ nullable: true })
  timeOrGap: string;

  @Column({ type: 'float', default: 0 })
  points: number;

  @Column({ default: false })
  isWildcard: boolean;

  @ManyToOne(() => Session, session => session.results)
  session: Relation<Session>;

  @ManyToOne(() => Driver, driver => driver.results)
  driver: Relation<Driver>;

  @ManyToOne(() => Team, team => team.results)
  team: Relation<Team>;

  @ManyToOne(() => Car, car => car.results)
  car: Relation<Car>;
}