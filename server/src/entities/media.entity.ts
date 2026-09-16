import { Entity, PrimaryGeneratedColumn, Column, ManyToOne } from 'typeorm';
import type { Relation } from 'typeorm';
import { Driver } from './driver.entity.js';
import { Team } from './team.entity.js';
import { Event } from './event.entity.js';
import { Car } from './car.entity.js';

@Entity('medias')
export class Media {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  type: string; // 'IMAGE', 'WIKIPEDIA_URL', etc.

  @Column()
  url: string;

  @Column({ nullable: true })
  caption: string;

  @ManyToOne(() => Driver, driver => driver.medias, { nullable: true })
  driver: Relation<Driver>;

  @ManyToOne(() => Team, team => team.medias, { nullable: true })
  team: Relation<Team>;

  @ManyToOne(() => Event, event => event.medias, { nullable: true })
  event: Relation<Event>;

  @ManyToOne(() => Car, car => car.medias, { nullable: true })
  car: Relation<Car>;
}