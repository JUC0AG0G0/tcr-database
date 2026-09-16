import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity('championships')
export class Championship {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  region: string;
}