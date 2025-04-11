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

/**
 * Asynchronously retrieves trip data from MongoDB.
 * @returns A promise that resolves to an array of Trip objects.
 */
export async function getTrips(): Promise<Trip[]> {
  // TODO: Implement this by connecting to MongoDB and fetching the data.

  return [
    {
      id: '1',
      timeOfDay: 'Morning',
      dayOfWeek: 'Monday',
      location: 'Downtown',
      demand: 100,
    },
    {
      id: '2',
      timeOfDay: 'Afternoon',
      dayOfWeek: 'Tuesday',
      location: 'Uptown',
      demand: 150,
    },
  ];
}
