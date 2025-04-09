import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type CourseDocument = Course & Document;

@Schema()
export class Course {
  @Prop({ required: true })
  name: string;

  @Prop({ required: true })
  description: string;

  @Prop({ type: [String], default: [] }) // Array de categorías
  categories: string[];

  @Prop({ required: true, unique: true })
  code: string;

  @Prop({ required: true, min: 0 }) // Precio no negativo
  price: number;

  @Prop({ enum: ['beginner', 'intermediate', 'advanced'], default: 'beginner' })
  level: string;
}

export const CourseSchema = SchemaFactory.createForClass(Course);
