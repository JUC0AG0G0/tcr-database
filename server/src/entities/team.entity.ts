import { Entity, PrimaryGeneratedColumn, Column, OneToMany, Relation } from 'typeorm';
import { Result } from './result.entity.js';
import { Media } from './media.entity.js';

@Entity('teams')
export class Team {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ nullable: true })
  nationality: string;

  @OneToMany(() => Result, result => result.team)
  results: Relation<Result>[];

  @OneToMany(() => Media, media => media.team)
  medias: Relation<Media>[];
}