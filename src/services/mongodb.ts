/**
 * Represents trip data.
 */
export interface Trip {
  /**
   * The unique identifier for the trip.
   */
  id: string;
  /**
   * The time of day when the trip occurred.
   */
  timeOfDay: string;
  /**
   * The day of the week when the trip occurred.
   */
  dayOfWeek: string;
  /**
   * The location where the trip started.
   */
  location: string;
  /**
   * The demand for trips at the time.
   */
  demand: number;
}

import { MongoClient, ServerApiVersion } from 'mongodb';

// Connection URI
const uri = process.env.MONGODB_URI;

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri!, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

/**
 * Asynchronously retrieves trip data from MongoDB.
 * @returns A promise that resolves to an array of Trip objects.
 */
export async function getTrips(): Promise<Trip[]> {
  try {
    // Connect the client to the server	(optional starting in v4.7)
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");

    const db = client.db('cabe'); // Replace with your actual database name
    const tripsCollection = db.collection<Trip>('trips'); // Replace with your actual collection name
    const trips = await tripsCollection.find().toArray();

    return trips;
  } catch(e) {
    console.error(e);
    return [];
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
