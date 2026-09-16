import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import type { Relation } from 'typeorm';
import { Result } from './result.entity.js';
import { Standing } from './standing.entity.js';
import { Media } from './media.entity.js';

@Entity('drivers')
export class Driver {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  firstName: string;

  @Column()
  lastName: string;

  @Column({ nullable: true })
  nationality: string;

  @Column({ type: 'date', nullable: true })
  dateOfBirth: string;

  @Column({ type: 'date', nullable: true })
  dateOfDeath: string;

  @Column({ type: 'text', nullable: true })
  biography: string;

  @Column({ nullable: true })
  instagram: string;

  @Column({ nullable: true })
  twitter: string;

  @Column({ nullable: true })
  youtube: string;

  @Column({ nullable: true })
  website: string;

  @OneToMany(() => Result, result => result.driver)
  results: Relation<Result>[];

  @OneToMany(() => Standing, standing => standing.driver)
  standings: Relation<Standing>[];

  @OneToMany(() => Media, media => media.driver)
  medias: Relation<Media>[];
}