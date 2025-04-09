import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type UserDocument = User & Document;

@Schema({ timestamps: true }) // Agrega `createdAt` y `updatedAt` automáticamente
export class User {
  @Prop({ required: true })
  firstname: string;

  @Prop({ required: true })
  lastname: string;

  @Prop({ required: true, unique: true })
  email: string;

  @Prop({ required: true })
  phoneNumber: string;

  @Prop({ default: Date.now })
  registrationDate: Date;

  @Prop({ enum: ['active', 'inactive'], default: 'active' })
  status: string;
}

export const UserSchema = SchemaFactory.createForClass(User);
