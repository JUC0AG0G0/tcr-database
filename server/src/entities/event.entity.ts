import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToMany } from 'typeorm';
import type { Relation } from 'typeorm';
import { Season } from './season.entity.js';
import { Session } from './session.entity.js';
import { Media } from './media.entity.js';

@Entity('events')
export class Event {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  circuit: string;

  @Column({ type: 'date', nullable: true })
  startDate: string;

  @Column({ type: 'date', nullable: true })
  endDate: string;

  @ManyToOne(() => Season, season => season.events)
  season: Relation<Season>;

  @OneToMany(() => Session, session => session.event)
  sessions: Relation<Session>[];

  @OneToMany(() => Media, media => media.event)
  medias: Relation<Media>[];
}