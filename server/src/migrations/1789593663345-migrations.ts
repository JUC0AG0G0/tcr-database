import { MigrationInterface, QueryRunner } from "typeorm";

export class Migrations1789593663345 implements MigrationInterface {
    name = 'Migrations1789593663345'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "championships" ("id" SERIAL NOT NULL, "name" character varying NOT NULL, "region" character varying NOT NULL, CONSTRAINT "PK_0f99e3669ee9b045b47cc8c916d" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "standings" ("id" SERIAL NOT NULL, "position" integer NOT NULL, "points" double precision NOT NULL, "seasonId" integer, "driverId" integer, CONSTRAINT "PK_ca695befaab9b01d05dd453dbdb" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "seasons" ("id" SERIAL NOT NULL, "year" integer NOT NULL, "championshipId" integer, CONSTRAINT "PK_cb8ed53b5fe109dcd4a4449ec9d" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "events" ("id" SERIAL NOT NULL, "name" character varying NOT NULL, "circuit" character varying NOT NULL, "startDate" date, "endDate" date, "seasonId" integer, CONSTRAINT "PK_40731c7151fe4be3116e45ddf73" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "sessions" ("id" SERIAL NOT NULL, "name" character varying NOT NULL, "type" character varying NOT NULL, "date" TIMESTAMP, "eventId" integer, CONSTRAINT "PK_3238ef96f18b355b671619111bc" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "teams" ("id" SERIAL NOT NULL, "name" character varying NOT NULL, "nationality" character varying, CONSTRAINT "PK_7e5523774a38b08a6236d322403" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "cars" ("id" SERIAL NOT NULL, "brand" character varying NOT NULL, "model" character varying NOT NULL, "year" integer, "isEvo" boolean NOT NULL DEFAULT false, CONSTRAINT "PK_fc218aa84e79b477d55322271b6" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "results" ("id" SERIAL NOT NULL, "startingPosition" integer, "finishPosition" integer, "status" character varying, "laps" integer, "timeOrGap" character varying, "points" double precision NOT NULL DEFAULT '0', "isWildcard" boolean NOT NULL DEFAULT false, "sessionId" integer, "driverId" integer, "teamId" integer, "carId" integer, CONSTRAINT "PK_e8f2a9191c61c15b627c117a678" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "drivers" ("id" SERIAL NOT NULL, "firstName" character varying NOT NULL, "lastName" character varying NOT NULL, "nationality" character varying, "dateOfBirth" date, "dateOfDeath" date, "biography" text, "instagram" character varying, "twitter" character varying, "youtube" character varying, "website" character varying, CONSTRAINT "PK_92ab3fb69e566d3eb0cae896047" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "medias" ("id" SERIAL NOT NULL, "type" character varying NOT NULL, "url" character varying NOT NULL, "caption" character varying, "driverId" integer, "teamId" integer, "eventId" integer, "carId" integer, CONSTRAINT "PK_f27321557a66cd4fae9bc1ed6e7" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "standings" ADD CONSTRAINT "FK_cfc3441ab9fd6c1f3fb9df36abe" FOREIGN KEY ("seasonId") REFERENCES "seasons"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "standings" ADD CONSTRAINT "FK_9e90a6b16067db8294ccee71880" FOREIGN KEY ("driverId") REFERENCES "drivers"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "seasons" ADD CONSTRAINT "FK_188d920abe9869560c52e0f7e44" FOREIGN KEY ("championshipId") REFERENCES "championships"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "events" ADD CONSTRAINT "FK_7bf7d324a2013e9d0b208ac2a82" FOREIGN KEY ("seasonId") REFERENCES "seasons"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "sessions" ADD CONSTRAINT "FK_61e25b191dd6844e30ff86e91ff" FOREIGN KEY ("eventId") REFERENCES "events"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "results" ADD CONSTRAINT "FK_4a3d55c4b43607aa72cf03dab38" FOREIGN KEY ("sessionId") REFERENCES "sessions"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "results" ADD CONSTRAINT "FK_63f79824443cb6743fe16c3f585" FOREIGN KEY ("driverId") REFERENCES "drivers"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "results" ADD CONSTRAINT "FK_3d4a3f7a5ea710a68f4bd7596e8" FOREIGN KEY ("teamId") REFERENCES "teams"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "results" ADD CONSTRAINT "FK_f63a43af46805658f4c13dde96c" FOREIGN KEY ("carId") REFERENCES "cars"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "medias" ADD CONSTRAINT "FK_2a60f3d13cd1c8551fb3c9a718a" FOREIGN KEY ("driverId") REFERENCES "drivers"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "medias" ADD CONSTRAINT "FK_fe519c57b3a7e16fd33bba26263" FOREIGN KEY ("teamId") REFERENCES "teams"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "medias" ADD CONSTRAINT "FK_729566435b461b7e48999e86a9d" FOREIGN KEY ("eventId") REFERENCES "events"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "medias" ADD CONSTRAINT "FK_32e3e25381b2f9440e88214e43b" FOREIGN KEY ("carId") REFERENCES "cars"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "medias" DROP CONSTRAINT "FK_32e3e25381b2f9440e88214e43b"`);
        await queryRunner.query(`ALTER TABLE "medias" DROP CONSTRAINT "FK_729566435b461b7e48999e86a9d"`);
        await queryRunner.query(`ALTER TABLE "medias" DROP CONSTRAINT "FK_fe519c57b3a7e16fd33bba26263"`);
        await queryRunner.query(`ALTER TABLE "medias" DROP CONSTRAINT "FK_2a60f3d13cd1c8551fb3c9a718a"`);
        await queryRunner.query(`ALTER TABLE "results" DROP CONSTRAINT "FK_f63a43af46805658f4c13dde96c"`);
        await queryRunner.query(`ALTER TABLE "results" DROP CONSTRAINT "FK_3d4a3f7a5ea710a68f4bd7596e8"`);
        await queryRunner.query(`ALTER TABLE "results" DROP CONSTRAINT "FK_63f79824443cb6743fe16c3f585"`);
        await queryRunner.query(`ALTER TABLE "results" DROP CONSTRAINT "FK_4a3d55c4b43607aa72cf03dab38"`);
        await queryRunner.query(`ALTER TABLE "sessions" DROP CONSTRAINT "FK_61e25b191dd6844e30ff86e91ff"`);
        await queryRunner.query(`ALTER TABLE "events" DROP CONSTRAINT "FK_7bf7d324a2013e9d0b208ac2a82"`);
        await queryRunner.query(`ALTER TABLE "seasons" DROP CONSTRAINT "FK_188d920abe9869560c52e0f7e44"`);
        await queryRunner.query(`ALTER TABLE "standings" DROP CONSTRAINT "FK_9e90a6b16067db8294ccee71880"`);
        await queryRunner.query(`ALTER TABLE "standings" DROP CONSTRAINT "FK_cfc3441ab9fd6c1f3fb9df36abe"`);
        await queryRunner.query(`DROP TABLE "medias"`);
        await queryRunner.query(`DROP TABLE "drivers"`);
        await queryRunner.query(`DROP TABLE "results"`);
        await queryRunner.query(`DROP TABLE "cars"`);
        await queryRunner.query(`DROP TABLE "teams"`);
        await queryRunner.query(`DROP TABLE "sessions"`);
        await queryRunner.query(`DROP TABLE "events"`);
        await queryRunner.query(`DROP TABLE "seasons"`);
        await queryRunner.query(`DROP TABLE "standings"`);
        await queryRunner.query(`DROP TABLE "championships"`);
    }

}
