import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const configService = app.get(ConfigService);
  console.log('MONGO_URI:', configService.get<string>('DATABASE_URL'));
  
  await app.listen(process.env.PORT ?? 3001);
}
bootstrap();
