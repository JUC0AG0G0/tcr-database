import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import type { Relation } from 'typeorm';
import { Result } from './result.entity.js';
import { Media } from './media.entity.js';

@Entity('cars')
export class Car {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  brand: string;

  @Column()
  model: string;

  @Column({ type: 'int', nullable: true })
  year: number;

  @Column({ default: false })
  isEvo: boolean;

  @OneToMany(() => Result, result => result.car)
  results: Relation<Result>[];

  @OneToMany(() => Media, media => media.car)
  medias: Relation<Media>[];
}