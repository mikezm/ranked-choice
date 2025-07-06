import React, { useState, ChangeEvent, FormEvent } from 'react';
import { Choice } from '../services/ballotService';
import { useCreateBallot } from '../hooks/useBallotQueries';

interface BallotFormProps {
  onSuccess: (slug: string) => void;
  onCancel: () => void;
}

interface FormValues {
  title: string;
  description: string;
  choices: Choice[];
}

interface FormErrors {
  title?: string;
  description?: string;
  choices?: string;
  choiceErrors?: { name?: string; description?: string }[];
}

const BallotForm: React.FC<BallotFormProps> = ({ onSuccess, onCancel }) => {
  const createBallotMutation = useCreateBallot();
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [formValues, setFormValues] = useState<FormValues>({
    title: '',
    description: '',
    choices: [
      { name: '', description: '' },
      { name: '', description: '' },
    ],
  });

  // Form errors state
  const [formErrors, setFormErrors] = useState<FormErrors>({
    choiceErrors: [{}, {}],
  });

  // Form touched state
  const [touched, setTouched] = useState({
    title: false,
    description: false,
    choices: [
      { name: false, description: false },
      { name: false, description: false },
    ],
  });

  // Validate form
  const validateForm = (values: FormValues): FormErrors => {
    const errors: FormErrors = {};
    const choiceErrors: { name?: string; description?: string }[] = [];

    // Validate title
    if (!values.title) {
      errors.title = 'Title is required';
    } else if (values.title.length > 255) {
      errors.title = 'Title must be at most 255 characters';
    }

    // Validate description
    if (values.description && values.description.length > 255) {
      errors.description = 'Description must be at most 255 characters';
    }

    // Validate choices
    if (!values.choices || values.choices.length === 0) {
      errors.choices = 'At least one choice is required';
    } else {
      values.choices.forEach((choice, index) => {
        const choiceError: { name?: string; description?: string } = {};

        if (!choice.name) {
          choiceError.name = 'Choice name is required';
        } else if (choice.name.length > 255) {
          choiceError.name = 'Choice name must be at most 255 characters';
        }

        if (choice.description && choice.description.length > 255) {
          choiceError.description = 'Choice description must be at most 255 characters';
        }

        choiceErrors[index] = choiceError;
      });
    }

    if (choiceErrors.some(error => Object.keys(error).length > 0)) {
      errors.choiceErrors = choiceErrors;
    }

    return errors;
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Validate form
    const errors = validateForm(formValues);
    setFormErrors(errors);

    // Mark all fields as touched
    setTouched({
      title: true,
      description: true,
      choices: formValues.choices.map(() => ({ name: true, description: true })),
    });

    // Check if there are any errors
    if (
      errors.title ||
      errors.description ||
      errors.choices ||
      (errors.choiceErrors && errors.choiceErrors.some(error => Object.keys(error).length > 0))
    ) {
      return;
    }

    // Submit form using react-query mutation
    setError(null);
    createBallotMutation.mutate(
      {
        title: formValues.title,
        description: formValues.description || undefined,
        choices: formValues.choices,
      },
      {
        onSuccess: slug => {
          onSuccess(slug);
        },
        onError: err => {
          setError('Failed to create ballot. Please try again.');
          console.error('Error submitting form:', err);
        },
      }
    );
  };

  // Handle input change
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;

    // Handle nested fields (choices)
    if (name.startsWith('choices[')) {
      const match = name.match(/choices\[(\d+)\]\.(\w+)/);
      if (match) {
        const index = parseInt(match[1], 10);
        const field = match[2];

        const newChoices = [...formValues.choices];
        newChoices[index] = {
          ...newChoices[index],
          [field]: value,
        };

        setFormValues({
          ...formValues,
          choices: newChoices,
        });
      }
    } else {
      // Handle regular fields
      setFormValues({
        ...formValues,
        [name]: value,
      });
    }
  };

  // Handle input blur
  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name } = e.target;

    // Handle nested fields (choices)
    if (name.startsWith('choices[')) {
      const match = name.match(/choices\[(\d+)\]\.(\w+)/);
      if (match) {
        const index = parseInt(match[1], 10);
        const field = match[2];

        const newTouched = { ...touched };
        if (!newTouched.choices[index]) {
          newTouched.choices[index] = { name: false, description: false };
        }
        newTouched.choices[index][field as keyof (typeof newTouched.choices)[0]] = true;

        setTouched(newTouched);

        // Validate on blur
        const errors = validateForm(formValues);
        setFormErrors(errors);
      }
    } else {
      // Handle regular fields
      setTouched({
        ...touched,
        [name]: true,
      });

      // Validate on blur
      const errors = validateForm(formValues);
      setFormErrors(errors);
    }
  };

  // Add a new choice field
  const addChoice = () => {
    setFormValues({
      ...formValues,
      choices: [...formValues.choices, { name: '', description: '' }],
    });

    setTouched({
      ...touched,
      choices: [...touched.choices, { name: false, description: false }],
    });
  };

  // Remove a choice field
  const removeChoice = (index: number) => {
    if (formValues.choices.length > 1) {
      const newChoices = [...formValues.choices];
      newChoices.splice(index, 1);

      setFormValues({
        ...formValues,
        choices: newChoices,
      });

      const newTouched = { ...touched };
      newTouched.choices.splice(index, 1);
      setTouched(newTouched);

      // Update errors
      const newErrors = { ...formErrors };
      if (newErrors.choiceErrors) {
        newErrors.choiceErrors.splice(index, 1);
        setFormErrors(newErrors);
      }
    }
  };

  return (
    <div className="ballot-form">
      <h2>Create New Ballot</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            type="text"
            onChange={handleChange}
            onBlur={handleBlur}
            value={formValues.title}
          />
          {touched.title && formErrors.title ? (
            <div className="error">{formErrors.title}</div>
          ) : null}
        </div>

        <div className="form-group">
          <label htmlFor="description">Description (optional)</label>
          <textarea
            id="description"
            name="description"
            onChange={handleChange}
            onBlur={handleBlur}
            value={formValues.description}
          />
          {touched.description && formErrors.description ? (
            <div className="error">{formErrors.description}</div>
          ) : null}
        </div>

        <h3>Choices</h3>
        {formErrors.choices && <div className="error">{formErrors.choices}</div>}
        {formValues.choices.map((choice: Choice, index: number) => (
          <div key={index} className="choice-container">
            <div className="form-group">
              <label htmlFor={`choices[${index}].name`}>Choice {index + 1} Name</label>
              <input
                id={`choices[${index}].name`}
                name={`choices[${index}].name`}
                type="text"
                onChange={handleChange}
                onBlur={handleBlur}
                value={choice.name}
              />
              {touched.choices?.[index]?.name && formErrors.choiceErrors?.[index]?.name ? (
                <div className="error">{formErrors.choiceErrors[index].name}</div>
              ) : null}
            </div>

            <div className="form-group">
              <label htmlFor={`choices[${index}].description`}>
                Choice {index + 1} Description (optional)
              </label>
              <input
                id={`choices[${index}].description`}
                name={`choices[${index}].description`}
                type="text"
                onChange={handleChange}
                onBlur={handleBlur}
                value={choice.description}
              />
              {touched.choices?.[index]?.description &&
              formErrors.choiceErrors?.[index]?.description ? (
                <div className="error">{formErrors.choiceErrors[index].description}</div>
              ) : null}
            </div>

            {formValues.choices.length > 1 && (
              <button
                type="button"
                onClick={() => removeChoice(index)}
                className="remove-choice-btn"
              >
                Remove Choice
              </button>
            )}
          </div>
        ))}

        <button type="button" onClick={addChoice} className="add-choice-btn">
          Add Another Choice
        </button>

        <div className="form-actions">
          <button type="button" onClick={onCancel} disabled={createBallotMutation.isLoading}>
            Cancel
          </button>
          <button type="submit" disabled={createBallotMutation.isLoading}>
            {createBallotMutation.isLoading ? 'Creating...' : 'Create Ballot'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BallotForm;
