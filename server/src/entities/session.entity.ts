import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToMany } from 'typeorm';
import type { Relation } from 'typeorm';
import { Event } from './event.entity.js';
import { Result } from './result.entity.js';

@Entity('sessions')
export class Session {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  type: string; // 'RACE' ou 'QUALIFYING'

  @Column({ type: 'timestamp', nullable: true })
  date: Date;

  @ManyToOne(() => Event, event => event.sessions)
  event: Relation<Event>;

  @OneToMany(() => Result, result => result.session)
  results: Relation<Result>[];
}