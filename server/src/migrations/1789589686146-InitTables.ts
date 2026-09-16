import { MigrationInterface, QueryRunner } from "typeorm";

export class InitTables1789589686146 implements MigrationInterface {
    name = 'InitTables1789589686146'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "championships" ("id" SERIAL NOT NULL, "name" character varying NOT NULL, "region" character varying NOT NULL, CONSTRAINT "PK_0f99e3669ee9b045b47cc8c916d" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "drivers" ("id" SERIAL NOT NULL, "firstName" character varying NOT NULL, "lastName" character varying NOT NULL, "nationality" character varying NOT NULL, "dateOfBirth" date, CONSTRAINT "PK_92ab3fb69e566d3eb0cae896047" PRIMARY KEY ("id"))`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DROP TABLE "drivers"`);
        await queryRunner.query(`DROP TABLE "championships"`);
    }

}
